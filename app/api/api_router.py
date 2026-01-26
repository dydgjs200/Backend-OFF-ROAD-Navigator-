from fastapi import APIRouter
from app.api.v1.endpoints import users, files

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["사용자"])
api_router.include_router(files.router, prefix="/files", tags=["파일"])