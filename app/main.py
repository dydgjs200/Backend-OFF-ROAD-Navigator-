import uuid
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db, engine, Base
from app.models.users import Users
from app.schemas.users import UserCreate

# 서버 실행 시 DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Off-Road Navigator API")

@app.get("/")
def main():
    return {"Hello": "World", "Project": "Off_Road Proj"}

@app.get("/health")
def health_check():
    return {"Status": "Ok"}

@app.post("/users/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. 중복 확인
    existing_user = db.query(Users).filter(Users.user_id == user_data.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")

    # 2. 데이터 생성
    new_user = Users(
        user_uuid=str(uuid.uuid4()),
        user_id=user_data.user_id,
        password=user_data.password  # 암호화는 다음 단계에서 적용!
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