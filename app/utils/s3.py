import boto3
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_S3_REGION")
)


def upload_file_to_s3(file, bucket_name):
    # 1. 파일 확장자 추출 및 고유 파일명 생성
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    try:
        # 2. S3 업로드 실행
        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            unique_filename,
            ExtraArgs={"ContentType": file.content_type}  # 브라우저에서 바로 볼 수 있게 설정
        )
        # 3. 업로드된 파일의 URL 반환
        return f"https://{bucket_name}.s3.{os.getenv('AWS_S3_REGION')}.amazonaws.com/{unique_filename}"
    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return None