import uuid
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FileUpLoadRequest(BaseModel):
    description: Optional[str] = Field(None, examples="비포장 도로 입구 사진")

class FileUpLoadResponse(BaseModel):
    user_uuid: uuid.UUID
    file_uuid: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_uuid: uuid.UUID
    created_at: datetime = Field(default_factory=datetime.now)

    # SQLAlchemy 사용을 위한 설정
    class Config:
        from_attributes = True