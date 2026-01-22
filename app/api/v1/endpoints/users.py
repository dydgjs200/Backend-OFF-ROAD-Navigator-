import os
import uuid
from http.client import HTTPException

from fastapi.params import Depends
from sqlalchemy.orm import Session

from fastapi import APIRouter, UploadFile, File

from app.db.session import get_db
from app.models.users import Users
from app.schemas.users import UserCreate

router = APIRouter()

@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. 중복확인
    existing_user = db.query(Users).filter(Users.user_id == user_data.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")

    # 2. 데이터 생성
    new_user = Users(
        user_uuid=str(uuid.uuid4()),
        user_id=user_data.user_id,
        password=user_data.password
    )

    # 3. DB 저장
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "회원가입 성공", "user_uuid": new_user.user_uuid}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
