from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from marshmallow import Schema, fields
from datetime import datetime, timezone


class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    reports = relationship('Report', backref='file', lazy=True)