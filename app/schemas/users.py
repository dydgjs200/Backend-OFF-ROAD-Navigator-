from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    user_id: str = Field(..., examples=["user1234"])
    password: str = Field(..., examples=["1234"])