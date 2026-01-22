import uuid
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os

from app.db.session import get_db, engine, Base
from app.models.users import Users
from app.schemas.users import UserCreate
from app.utils.s3 import upload_file_to_s3
from app.api.api_router import api_router

# 서버 실행 시 DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Off-Road Navigator API")

# api_router 등록
app.include_router(api_router, prefix="/api")

@app.get("/")
def main():
    return {"Hello": "World", "Project": "Off_Road Proj"}

@app.get("/health")
def health_check():
    return {"Status": "Ok"}
