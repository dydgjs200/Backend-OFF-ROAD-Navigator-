import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import CHAR, VARCHAR
from datetime import datetime
from app.db.session import Base

class Files(Base):
    __tablename__ = "files"

    file_uuid = Column(CHAR(36), primary_key=True, nullable=False)
    file_path = Column(VARCHAR(200), nullable=False)        # S3 파일경로
    created_at = Column(DateTime, default=datetime.now)