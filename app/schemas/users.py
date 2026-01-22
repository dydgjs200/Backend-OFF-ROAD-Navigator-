from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    user_id: str = Field(..., examples=["user1234"])
    password: str = Field(..., min_length=4, max_length=64, examples=["1234"])