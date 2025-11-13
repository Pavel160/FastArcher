from app.api.routes.utils.error_response import exception_service
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db
from app.services.file_upload_service import UploadService

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/{telegram_id}")
async def upload_csv(telegram_id: int, file: UploadFile, db: AsyncSession = Depends(get_async_db)):
    """Загружает файл CSV"""
    return await exception_service(UploadService.process_csv_upload, telegram_id, file, db)

