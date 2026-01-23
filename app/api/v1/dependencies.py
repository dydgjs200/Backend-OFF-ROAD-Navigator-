from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.users import Users
import os

# 스웨거에 토큰 보내는 곳 명시
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="로그인이 필요한 서비스입니다.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        # 1. 토큰 해독
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        user_uuid: str = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # 2. 활성화 된 유저인지 확인
    user = db.query(Users).filter(Users.user_uuid == user_uuid, Users.active == True)
    if user is None:
        raise credentials_exception

    return user