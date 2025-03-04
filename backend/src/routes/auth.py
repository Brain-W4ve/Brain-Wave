from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils.auth_utils import encode_auth_token, decode_auth_token, token_required
from ..utils.utils import validate_schema
from ..models import BLacklist_Token, User
from ..schemas.auth import *
from src.db import Session_Factory

auth_bp = Blueprint("auth", __name__)

register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()
user_schema = UserSchema()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # maybe you can create this as a decorator
    user_data, error = validate_schema(register_schema, data)
    if error:
        return error
    
    with Session_Factory() as session_:
        if session_.query(User).filter_by(email=user_data["email"]).first():
            return jsonify({"message": "User already exists"}), 400
        
        new_user = User(**{**user_data, "password": generate_password_hash(user_data["password"])})
        session_.add(new_user)
        session_.commit()

        auth_token = encode_auth_token(new_user.id, current_app.config["SECRET_KEY"])

    return jsonify({
            "message": "Successfully registered",
            "user": user_schema.dump(new_user),
            "auth_token": auth_token
        })
    
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    login_data, error = validate_schema(login_schema, data)
    if error:
        return error, 400

    with Session_Factory() as session_:
        user = session_.query(User).filter_by(email=login_data["email"]).first()

        if user and check_password_hash(user.password, login_data["password"]):
            auth_token = encode_auth_token(user.id, current_app.config["SECRET_KEY"])
            return jsonify({"message": "Login successful", "auth_token": auth_token}), 200
        
        return jsonify({"message": "Invalid credentials"}), 401
    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")
    if not auth_header or " " not in auth_header:
        return jsonify({"message": "Missing or invalid Authorization header"}), 401

    auth_token = auth_header.split(" ")[1]

    with Session_Factory() as session_:
        resp = decode_auth_token(auth_token, current_app.config["SECRET_KEY"], session_)

        if isinstance(resp, str):  # If it's an error message
            return jsonify({"message": resp}), 401

        # Check if token is already blacklisted
        if session_.query(BLacklist_Token).filter_by(token=auth_token).first():
            return jsonify({"message": "Token already blacklisted"}), 400

        # Blacklist the token
        blacklist_token = BLacklist_Token(token=auth_token)
        session_.add(blacklist_token)
        session_.commit()

        return jsonify({"message": "Successfully logged out"}), 200



@auth_bp.route("/status")
@token_required
def get_status(user_id):
    with Session_Factory() as session_:
        user = session_.query(User).filter_by(id=user_id).first()
        if user:
            return jsonify({
                "status": "success",
                "data": user_schema.dump(user)
            })
        else:
            return jsonify({
                "status": "fail",
                "message": "User not found"
            }), 404