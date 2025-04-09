from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from . import Base


class ProcessedFile(Base):
    __tablename__ = "processed_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    processed_filename = Column(String, nullable=False)
    processed_date = Column(DateTime, default=datetime.now(timezone.utc))
    model_id = Column(Integer, ForeignKey("ml_models.id"), nullable=False)

    original_file = relationship("File", back_populates="processed_files")
    model = relationship("MLModel", back_populates="processed_files")