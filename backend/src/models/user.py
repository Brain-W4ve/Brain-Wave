from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base
from marshmallow import Schema, fields
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(200), nullable=False)

    # Relationships
    files = relationship('File', backref='user', lazy=True, cascade="all, delete")
    reports = relationship('Report', backref='user', lazy=True, cascade="all, delete")
