from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_POOL_TIMEOUT = 30

engine = create_engine(
    DATABASE_URL,
    pool_size=SQLALCHEMY_POOL_SIZE,
    pool_timeout=SQLALCHEMY_POOL_TIMEOUT,
    pool_recycle=3600
)

Session_Factory = sessionmaker(autoflush=False, autocommit=False, bind=engine)