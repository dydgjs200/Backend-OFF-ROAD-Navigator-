import os
import uuid
from http.client import HTTPException
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_current_user
from app.db.session import get_db
from app.utils.s3 import upload_file_to_s3
from app.models.users import Users
from app.models.files import Files
from app.schemas.fileUpload import FileUpLoadResponse

router = APIRouter()

@router.post("/files", response_model=FileUpLoadResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    # 이미지 파일인지 체크
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    file_url = upload_file_to_s3(file, bucket_name)

    if not file_url:
        raise HTTPException(status_code=500, detail="S3 업로드에 실패했습니다.")

    new_file = Files(
        file_uuid=str(uuid.uuid4()),
        file_path=file_url,
        user_uuid=current_user.user_uuid,
        created_at=datetime.now()
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file