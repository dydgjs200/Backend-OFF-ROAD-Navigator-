import os
from http.client import HTTPException

from fastapi import APIRouter, UploadFile, File
from app.utils.s3 import upload_file_to_s3

router = APIRouter()

@router.post("/files")
async def upload_file(file: UploadFile = File(...)):
    # 이미지 파일인지 체크
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    file_url = upload_file_to_s3(file, bucket_name)

    if not file_url:
        raise HTTPException(status_code=500, detail="S3 업로드에 실패했습니다.")

    return {
        "message": "업로드 성공",
        "file_url": file_url
    }