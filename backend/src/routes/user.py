from flask import Blueprint, request, jsonify, flash, session
from models.user import User, User_Schema
from models import Base
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user


user_bp = Blueprint('users', __name__)


from sqlalchemy import create_engine
from dotenv import load_dotenv
import os



engine = create_engine(os.getenv("DATABSE_URL", "sqlite:///data.db"), future=True)
Base.metadata.create_all(engine)

@user_bp.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']

    with Session(engine) as session_:
        if session_.query(User).filter_by(username=username).first():
            return jsonify({"message": "User already taken"}, 400)
        
        new_user = User(username=username, password=generate_password_hash(password))
        session_.add(new_user)
        session_.commit()
        return jsonify({"user"}, 200)
    
@user_bp.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    with Session(engine) as session_:
        user = session_.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            session['user_id'] = user.id
            return jsonify(204)
        return jsonify({}, 400)
    
@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return jsonify({}, 200)