from app.api.routes.utils.error_response import exception_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db
from app.api.schemas.user_schema import (
    PasswordUpdate, RegisterRequest, RegisterResponse, UsernameUpdate, VerifyRequest,
    VerifyResponse, UserLogin, UserResponse
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=RegisterResponse)
async def register_user(data: RegisterRequest, db: AsyncSession = Depends(get_async_db)):
    """Регистрирует нового пользователя."""
    return await exception_service(UserService.register_user, data, db)


@router.post("/verify", response_model=RegisterResponse)
async def verify_user(data: VerifyRequest, db: AsyncSession = Depends(get_async_db)):
    """Подтверждает регистрацию пользователя с помощью кода."""
    return await exception_service(UserService.verify_user, data, db)


@router.post("/login", response_model=VerifyResponse)
async def login_user(data: UserLogin, db: AsyncSession = Depends(get_async_db)):
    """Выполняет вход пользователя в систему."""
    return await exception_service(UserService.login_user, data, db)


@router.post("/logout", response_model=VerifyResponse)
async def logout_user(telegram_id: int, db: AsyncSession = Depends(get_async_db)):
    """Выполняет выход пользователя из системы."""
    return await exception_service(UserService.logout_user, telegram_id, db)


@router.get("/{telegram_id}", response_model=UserResponse)
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_async_db)):
    """Получает информацию о пользователе по его Telegram ID."""
    return await exception_service(UserService.get_user, telegram_id, db)


@router.patch("/{telegram_id}/password", response_model=UserResponse)
async def change_password(data: PasswordUpdate, db: AsyncSession = Depends(get_async_db)):
    """Изменяет пароль пользователя."""
    return await exception_service(UserService.change_password, data, db)


@router.patch("/{telegram_id}/username", response_model=UserResponse)
async def change_username(data: UsernameUpdate, db: AsyncSession = Depends(get_async_db)):
    """Изменяет имя пользователя (логин)."""
    return await exception_service(UserService.change_username, data, db)
