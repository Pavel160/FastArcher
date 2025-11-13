from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.user_summaries_model import UserSummary
from app.daos.base_dao import BaseDAO


class UserSummaryDAO(BaseDAO[UserSummary]):
    model = UserSummary

    @staticmethod
    async def get_summary_by_user_id(user_id: int, session: AsyncSession) -> Optional[UserSummary]:
        """Получает запись UserSummary по уникальному идентификатору пользователя (User ID)."""
        stmt = select(UserSummary).where(UserSummary.user_id == user_id)
        return await session.scalar(stmt)

    @staticmethod
    async def get_or_create_summary(user_id, username, session: AsyncSession) -> UserSummary:
        """Получает или создает запись UserSummary для пользователя."""
        stmt = select(UserSummary).where(UserSummary.user_id == user_id)
        summary = await session.scalar(stmt)

        if not summary:
            summary = UserSummary(
                user_id=user_id,
                username=username,
                sessions=0,
                shots=0,
                average_score=0.0
            )
            session.add(summary)
            await session.flush()
        return summary
