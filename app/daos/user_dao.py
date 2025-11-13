from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.user_model import User
from app.daos.base_dao import BaseDAO


class UserDAO(BaseDAO[User]):
    model = User

    @staticmethod
    async def get_by_username(username: str, session: AsyncSession) -> User:
        """Находит пользователя по уникальному имени пользователя."""
        stmt = select(User).where(User.username == username)
        return await session.scalar(stmt)

    @staticmethod
    async def get_by_telegram_id(telegram_id: int, session: AsyncSession) -> User:
        """Находит пользователя по уникальному идентификатору Telegram ID."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        return await session.scalar(stmt)

    @staticmethod
    async def get_by_username_and_tg(username: str, telegram_id: int, session: AsyncSession):
        """Возвращает пользователя по username и Telegram ID."""
        stmt = select(User).where(User.username == username, User.telegram_id == telegram_id)
        return await session.scalar(stmt)


    @staticmethod
    async def get_active_user_by_telegram_id(telegram_id: int, session: AsyncSession):
        """Возвращает активного пользователя по Telegram ID."""
        stmt = select(User).where(User.telegram_id == telegram_id, User.is_active == True)
        return await session.scalar(stmt)

    @staticmethod
    async def deactivate_all_by_tg(telegram_id: int, session: AsyncSession):
        """Деактивирует все аккаунты с данным Telegram ID."""
        await session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(is_active=False)
        )
        await session.commit()
