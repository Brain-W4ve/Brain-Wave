from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

# I believe files should have their reports, and user can access their reports by accessing its files

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Integer, primary_key=True, unique=True) # should this be primary key?
    username = Column(String(255), nullable=False)
    password = Column(String(200), nullable=False)

    # Relationships
    # files = relationship('File', backref='user', lazy=True, cascade="all, delete")
    # reports = relationship('Report', backref='user', lazy=True, cascade="all, delete")


    # Maybe have:

    @staticmethod
    def encode_auth_token(user_id, secret_key):
        ...
    
    @staticmethod
    def decode_auth_token(auth_token, secret_key, session):
        ...
