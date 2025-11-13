import aiohttp
from app.bot.utils.response_to_error import errors_service
from app.core.config import settings


API_HOST = settings.api.API_HOST
API_INTERNAL_PORT = settings.api.API_INTERNAL_PORT
API_URL = f"http://{API_HOST}:{API_INTERNAL_PORT}"

async def api_get_total_sessions(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/stats/total_sessions/{user_id}")as resp:
            return await errors_service(resp, "Данные о сессиях не найдены.")


async def api_get_average_score(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/stats/average_score/{user_id}")as resp:
            return await errors_service(resp, "Данные о выстрелах не найдены.")


async def api_get_total_shots(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/stats/total_shots/{user_id}")as resp:
            return await errors_service(resp, "Данные о выстрелах не найдены.")


async def api_get_best_session(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/stats/best_session/{user_id}")as resp:
            return await errors_service(resp, "Данные о сессиях не найдены.")


async def api_get_last_session_date(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/stats/last_session_date/{user_id}")as resp:
            return await errors_service(resp, "Данные о датах не найдены.")
