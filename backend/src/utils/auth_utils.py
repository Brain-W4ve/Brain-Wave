import datetime
import jwt
from ..models import BLacklist_Token

from functools import wraps
from flask import request, jsonify, current_app
from sqlalchemy.orm import Session
from src.db import Session_Factory

def encode_auth_token(user_id, secret_key) -> str:
    """
    Generates the Auth token
    :return string
    """

    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            "exp": now + datetime.timedelta(days=0, hours=0, minutes=30),
            "iat": now,
            "sub": str(user_id)
        }

        return jwt.encode(
            payload,
            secret_key,
            "HS256"
        )

    except Exception as e:
        return e
    
def decode_auth_token(auth_token, secret_key, session) -> int | str:
    """
    Decodes the auth token
    :param auth_token: string
    :return: integer|string
    """

    try:
        # payload = jwt.decode(auth_token, secret_key)
        payload = jwt.decode(auth_token, secret_key, "HS256")
        is_blacklisted_token = BLacklist_Token.check_blacklist(auth_token, session)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again'
        else:
            return int(payload["sub"])
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError as e:
        return "Invalid token. Please log in again."


# auth decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            return jsonify({
                "status": "fail",
                "message": "Provide a valid auth token"
            }), 401
        
        with Session_Factory() as session_:
            resp = decode_auth_token(auth_token, current_app.config["SECRET_KEY"], session_)

            if isinstance(resp, str):
                return jsonify({
                    "status": "fail",
                    "message": resp
                }), 401
            
            return f(*args, **kwargs, user_id=resp)
    return decorator
        