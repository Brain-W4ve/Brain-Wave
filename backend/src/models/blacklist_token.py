from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from . import Base
import datetime
from flask import current_app


class BLacklist_Token(Base):
    __tablename__ = "blacklist_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def check_blacklist(auth_token, session):
        return session.query(BLacklist_Token).filter_by(token=auth_token).scalar() is not None
