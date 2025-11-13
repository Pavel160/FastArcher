from typing import Optional
from app.core.config import settings
from app.models import *
from app.models.base_model import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)


DB_USER = settings.postgres.DB_USER
DB_PASSWORD = settings.postgres.DB_PASSWORD
DB_HOST = settings.postgres.DB_HOST
DB_INTERNAL_PORT = settings.postgres.DB_INTERNAL_PORT
DB_NAME = settings.postgres.DB_NAME


class PostgresClient:
    """
    Асинхронный клиент PostgreSQL на основе SQLAlchemy.
    Предоставляет сессии для работы с базой данных.
    """

    def __init__(self):
        """
        Инициализирует атрибуты как None, чтобы они были готовы к подключению.
        """
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[sessionmaker] = None

    async def connect(self):
        """
        Устанавливает соединение с базой данных.
        """
        if self.engine is None:
            self.engine = create_async_engine(
                "postgresql+asyncpg://",
            connect_args={
                "user": DB_USER,
                "password": DB_PASSWORD,
                "host": DB_HOST,
                "port": DB_INTERNAL_PORT,
                "database": DB_NAME
    },
            echo=False,
)
            self.session_factory = sessionmaker(
                self.engine,
                expire_on_commit=False,
                class_=AsyncSession
            )

            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        """
        Генератор асинхронной сессии для работы с PostgreSQL.
        """
        async with self.session_factory() as session:
            yield session

    async def disconnect(self):
        """
        Полностью закрывает пул соединений.
        """
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None

    def get_engine(self) -> AsyncEngine:
        """
        Возвращает движок SQLAlchemy.
        """
        return self.engine


# Глобальный экземпляр клиента
postgres_client = PostgresClient()
