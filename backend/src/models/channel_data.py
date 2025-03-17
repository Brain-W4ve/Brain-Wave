from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class Channel_Data(Base):
    __tablename__ = "channel_data"

    id = Column(Integer, primary_key=True)
    channel_number = Column(Integer, nullable=False)
    sampling_rate = Column(Float, nullable=False)
    data = Column(Text, nullable=False) # store as json string
    file_id = Column(Integer, ForeignKey('file_data.id'), nullable=False)

    file = relationship("File_Data", back_populates="channels")