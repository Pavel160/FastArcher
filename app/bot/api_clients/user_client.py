import aiohttp
from app.bot.utils.response_to_error import errors_service
from app.core.config import settings


API_HOST = settings.api.API_HOST
API_INTERNAL_PORT = settings.api.API_INTERNAL_PORT
API_URL = f"http://{API_HOST}:{API_INTERNAL_PORT}"

async def api_register_user(username: str, password: str, telegram_id: int):
    """Регистрирует нового пользователя на сервере API."""
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/users/register", json={
            "username": username,
            "password": password,
            "telegram_id": telegram_id}) as resp:
            return await errors_service(resp, "Ошибка регистрации")


async def api_verify_user(username: str, telegram_id: int, code: str):
    """Подтверждает учетную запись пользователя с помощью кода верификации."""
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/users/verify", json={
            "username": username,
            "telegram_id": telegram_id,
            "code": code}) as resp:
            return await errors_service(resp, "Ошибка проверки кода")
 

async def api_login_user(username: str, password: str, telegram_id: int):
    """Аутентифицирует пользователя и выполняет вход."""
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/users/login", json={
            "username": username,
            "password": password,
            "telegram_id": telegram_id}) as resp:
            return await errors_service(resp, "Ошибка входа")


async def api_logout_user(telegram_id: int):
    """Выполняет выход пользователя из системы (отзывает сессию, связанную с telegram_id)."""
    async with aiohttp.ClientSession() as session:
        params = {"telegram_id": telegram_id}
        async with session.post(f"{API_URL}/users/logout", params=params) as resp:
            return await errors_service(resp, "Ошибка при выходе")


async def api_update_username(telegram_id: int, new_username: str):
    """Обновляет имя пользователя на новое."""
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL}/users/{telegram_id}/username", json={
                "telegram_id": telegram_id,
                "new_username": new_username}) as resp:
            return await errors_service(resp, "Ошибка при смене имени")


async def api_update_password(telegram_id: int, new_password: str):
    """Обновляет пароль пользователя."""
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL}/users/{telegram_id}/password", json={
                "telegram_id": telegram_id,
                "new_password": new_password}) as resp:
            return await errors_service(resp, "Ошибка при смене пароля")


async def api_get_user(telegram_id: int):
    """Получает детальную информацию о пользователе по его Telegram ID."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/users/{telegram_id}")as resp:
            return await errors_service(resp, "Ошибка при получении пользователя")
