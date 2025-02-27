import datetime
import jwt
from ..models import BLacklist_Token

def encode_auth_token(user_id, secret_key) -> str:
    """
    Generates the Auth token
    :return string
    """

    try:
        now = datetime.timezone.utc
        payload = {
            "exp": now + datetime.timedelta(days=0, hours=0, minutes=30),
            "iat": now,
            "sub": user_id
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
        payload = jwt.decode(auth_token, secret_key)
        is_blacklisted_token = BLacklist_Token.check_blacklist(auth_token, session)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again'
        else:
            return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
