from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base
import datetime
import jwt
from .blacklist_token import BLacklist_Token

# I believe files should have their reports, and user can access their reports by accessing its files

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True) # should this be primary key?
    username = Column(String(255), nullable=False)
    password = Column(String(200), nullable=False)

    # Relationships
    # files = relationship('File', backref='user', lazy=True, cascade="all, delete")
    files = relationship('File', back_populates='user', cascade='all, delete')
    # reports = relationship('Report', backref='user', lazy=True, cascade="all, delete")


    # Maybe have:

    @staticmethod
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
    
    @staticmethod
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
