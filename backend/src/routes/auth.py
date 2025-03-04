from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Session
from ..utils.auth_utils import encode_auth_token, decode_auth_token
from ..models import BLacklist_Token, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    engine = current_app.config["DB_ENGINE"]

    with Session(engine) as session_:
        if session_.query(User).filter_by(email=email).first():
            return jsonify({"message": "User already exists"}), 400
        

        new_user = User(username=username, email=email, password=generate_password_hash(password))
        session_.add(new_user)
        session_.commit()

        auth_token = encode_auth_token(new_user.id, current_app.config["SECRET_KEY"])

        return jsonify({
            "message": "Successfully registered", 
            "auth_token": auth_token
        })
    
@auth_bp.route("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    engine = current_app.config["DB_ENGINE"]

    with Session(engine) as session_:
        user = session_.query(User).filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            auth_token = encode_auth_token(user.id, current_app.config["SECRET_KEY"])
            return jsonify({"message": "Login successful", "auth_token": auth_token}), 200
        
        return jsonify({"message": "Invalid credentials"}), 401
    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ""

    if auth_token:
        engine = current_app.config["DB_ENGINE"]
        with Session(engine) as session_:
            resp = decode_auth_token(auth_token, current_app.config["SECRET_KEY"], session_)
            if not isinstance(resp, Exception):
                # mark the token as blacklisted
                blacklist_token = BLacklist_Token(token=auth_token)
                try:
                    session_.add(blacklist_token)
                    session_.commit()
                    return jsonify({"message": "Successfully logged out"})
                except Exception as e:
                    return jsonify({"message": f"Error: {e}"}), 400
            else:
                return jsonify({"message": f"Error decoded token: {resp} is not string"})
    else:
        return jsonify({"message": "Provide a valid auth token"}), 401
    
@auth_bp.route("/status")
def get_status():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ""

    if auth_token:
        engine = current_app.config["DB_ENGINE"]
        with Session(engine) as session_:
            resp = decode_auth_token(auth_token, current_app.config["SECRET_KEY"], session_)
            if not isinstance(resp, Exception):
                user = session_.query(User).filter_by(id=resp).first()
                return jsonify({
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "email": user.email,
                    }
                }), 200
            else:
                return jsonify({
                    "status": "fail",
                    "message": resp
                }), 401
    else:
        return jsonify({
            "status": "fail",
            "message": "Provide a valid auth token"
        }), 401