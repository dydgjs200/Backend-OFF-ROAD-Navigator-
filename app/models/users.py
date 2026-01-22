import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime
from app.db.session import Base

class Users(Base):
    __tablename__ = "users"

    user_uuid = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)