from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from marshmallow import Schema, fields
from datetime import datetime, timezone


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    generated_date = Column(DateTime, default=datetime.now(timezone.utc))
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    data = Column() # report data