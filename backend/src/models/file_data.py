from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from . import Base

class File_Data(Base):
    __tablename__ = "file_data"
    id = Column(Integer, primary_key=True)
    # timestamp = Column(DateTime, nullable=False)
    filename = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)