import random
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.daos.user_dao import UserDAO
from app.api.schemas.user_schema import (
    PasswordUpdate, RegisterRequest, RegisterResponse, UserCreate,
    UserLogin, UserResponse, UsernameUpdate, VerifyRequest, VerifyResponse
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Сервис управления пользователями (основная логика)."""
    @staticmethod
    async def register_user(data: RegisterRequest, db: AsyncSession) -> RegisterResponse:
        """Регистрирует нового пользователя в системе."""
        existing_by_username = await UserDAO.get_by_username(data.username, db)
        if existing_by_username:
            raise ValueError(f"Имя пользователя '{data.username}' уже занято. Попробуйте другое.")

        verification_code = str(random.randint(1000, 9999))
        password_hash = pwd_context.hash(data.password)

        new_user = UserCreate(
            username=data.username,
            password_hash=password_hash,
            telegram_id=data.telegram_id,
            verification_code=verification_code,
            is_active=False
        )
        await UserDAO.create(db, new_user)

        return RegisterResponse(
            message=f"Пользователь '{data.username}' успешно зарегистрирован!",
            verification_code=verification_code
        )


    @staticmethod
    async def verify_user(data: VerifyRequest, db: AsyncSession) -> VerifyResponse:
        """Подтверждает пользователя по коду."""
        user = await UserDAO.get_by_username_and_tg(data.username, data.telegram_id, db)
        if not user:
            raise ValueError("Пользователь не найден.")

        if user.verification_code != data.code:
            raise ValueError("Неверный код подтверждения.")

        user.verification_code = None
        await db.commit()
        await db.refresh(user)

        return VerifyResponse(message=f"Пользователь {user.username} успешно подтверждён!", verification_code=None)


    @staticmethod
    async def login_user(data: UserLogin, db: AsyncSession) -> VerifyResponse:
        """Аутентифицирует пользователя по имени и паролю."""

        user = await UserDAO.get_by_username_and_tg(data.username, data.telegram_id, db)
        if not user:
            raise ValueError("Пользователь не найден. Сначала зарегистрируйтесь.")

        if not pwd_context.verify(data.password, user.password_hash):
            raise ValueError("Неверное имя пользователя или пароль.\n"
                            "Введите имя пользователя: ")

        if user.is_active:
            return VerifyResponse(message=f"Вы уже вошли в систему как {user.username}")


        await UserDAO.deactivate_all_by_tg(data.telegram_id, db)

        user.is_active = True
        await db.commit()
        await db.refresh(user)

        return VerifyResponse(message=f"Добро пожаловать, {user.username}!")


    @staticmethod
    async def logout_user(telegram_id: int, db: AsyncSession) -> VerifyResponse:
        """Выводит активного пользователя из системы."""
        user = await UserDAO.get_active_user_by_telegram_id(telegram_id, db)
        if not user:
            raise ValueError("Вы не вошли ни в один аккаунт.")

        user.is_active = False
        await db.commit()
        await db.refresh(user)

        return VerifyResponse(message="Вы успешно вышли из системы.")


    @staticmethod
    async def change_username(data: UsernameUpdate, db: AsyncSession) -> UserResponse:
        """Изменяет имя текущего активного пользователя."""
        user = await UserDAO.get_active_user_by_telegram_id(data.telegram_id, db)
        if not user:
            raise ValueError("Сначала войдите в аккаунт.")

        existing = await UserDAO.get_by_username(data.new_username, db)
        if existing:
            raise ValueError("Имя пользователя уже занято.")

        user.username = data.new_username
        await db.commit()
        await db.refresh(user)

        return UserResponse(id=user.id, username=user.username, is_active=user.is_active)


    @staticmethod
    async def change_password(data: PasswordUpdate, db: AsyncSession) -> UserResponse:
        """Изменяет пароль активного пользователя."""
        user = await UserDAO.get_active_user_by_telegram_id(data.telegram_id, db)
        if not user:
            raise ValueError("Сначала войдите в аккаунт.")

        user.password_hash = pwd_context.hash(data.new_password)
        await db.commit()
        await db.refresh(user)

        return UserResponse(id=user.id, username=user.username, is_active=user.is_active)


    @staticmethod
    async def get_user(telegram_id: int, db: AsyncSession) -> UserResponse:
        """Получение профиля по telegram_id. ."""
        user = await UserDAO.get_active_user_by_telegram_id(telegram_id, db)
        if not user:
            raise ValueError("Пользователь не найден.")
        return UserResponse(id=user.id, username=user.username, is_active=user.is_active)
