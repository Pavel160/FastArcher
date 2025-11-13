import aiohttp
from app.bot.utils.response_to_error import errors_service
from app.core.config import settings


API_HOST = settings.api.API_HOST
API_INTERNAL_PORT = settings.api.API_INTERNAL_PORT
API_URL = f"http://{API_HOST}:{API_INTERNAL_PORT}"

async def api_upload_csv(file_data: bytes, filename: str, telegram_id: int):
    """Загружает CSV-файл  для обработки."""
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("file", file_data, filename=filename, content_type="text/csv")
        async with session.post(f"{API_URL}/upload/{telegram_id}", data=form) as resp:
            return await errors_service(resp, "Ошибка при загрузке CSV")
