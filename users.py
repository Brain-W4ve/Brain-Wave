from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    email = Column(String(100), primary_key=True)  # 🔹 Clave primaria
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)  # 🔹 Se almacena como hash

    def __repr__(self):
        return f"<User(email={self.email}, name={self.name})>"
