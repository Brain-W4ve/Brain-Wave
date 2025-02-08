from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from . import Base
from marshmallow import Schema, fields

class File_Data(Base):
    __tablename__ = "file_data"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    channels = relationship("Channel_Data", back_populates="file", cascade="all, delete-orphan")

class File_Data_Schema(Schema):
    id = fields.Int()
    filename = fields.Str()