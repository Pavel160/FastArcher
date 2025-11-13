from app.core.database import postgres_client
from sqlalchemy.ext.asyncio import AsyncSession

# Определяем функцию-зависимость для FastAPI
async def get_async_db() -> AsyncSession:
    """
    Предоставляет асинхронную сессию БД для использования в роутерах.
    """
    async with postgres_client.session_factory() as session:
        yield session
