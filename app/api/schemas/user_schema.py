from pydantic import BaseModel, ConfigDict
from typing import Optional

#  Регистрация
class RegisterRequest(BaseModel):
    username: str
    password: str
    telegram_id: int

class RegisterResponse(BaseModel):
    message: str
    verification_code: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

#  Верификация
class VerifyRequest(BaseModel):
    username: str
    telegram_id: int
    code: str

class VerifyResponse(BaseModel):
    message: str
    verification_code: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Пользователь
class UserCreate(BaseModel):
    username: str
    password_hash: str
    telegram_id: int
    verification_code: str
    is_active: bool

class UserLogin(BaseModel):
    username: str
    password: str
    telegram_id: int

class UsernameUpdate(BaseModel):
    telegram_id: int
    new_username: str

class PasswordUpdate(BaseModel):
    telegram_id: int
    new_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
