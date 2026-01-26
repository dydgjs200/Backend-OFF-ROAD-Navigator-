import os
import uuid
from http.client import HTTPException

from fastapi.params import Depends
from sqlalchemy.orm import Session

from fastapi import APIRouter, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.models.users import Users
from app.schemas.users import UserCreate
from app.utils.encrypt import get_password_hash, verify_password
from app.utils.jwt import create_jwt


router = APIRouter()

@router.post("/create_user")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. 중복확인
    existing_user = db.query(Users).filter(Users.user_id == user_data.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")

    # 2. 데이터 생성
    new_user = Users(
        user_uuid=str(uuid.uuid4()),
        user_id=user_data.user_id,
        password=get_password_hash(user_data.password)
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

# soft delete 추가
@router.delete("/delete_user/{user_uuid}")
def delete_user(user_uuid: str, db: Session = Depends(get_db)):
    # 1. 유저 존재 확인
    user = db.query(Users).filter(Users.user_uuid == user_uuid).first()

    if not user:
        raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")

    try:
        user.active = False
        db.commit()
        return {"message": "회원 탈퇴가 완료되었습니다."}
    except Exception as e:
        db.rollback()  # 오류 시 작업 취소
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@router.post("/login")
def login(
        # 기존 UserLogin 대신 OAuth2PasswordRequestForm을 사용합니다.
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    # 1. 유저 확인 (form_data.username 사용)
    user = db.query(Users).filter(
        Users.user_id == form_data.username,  # user_id가 아닌 username으로 들어옵니다.
        Users.active == True
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")

    # 2. 유저 비밀번호 확인 (form_data.password 사용)
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")

    # 3. JWT 발급
    access_token = create_jwt(data={"sub": user.user_uuid})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_uuid": user.user_uuid
    }