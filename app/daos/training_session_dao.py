from sqlalchemy.ext.asyncio import AsyncSession
from app.models.training_session_model import TrainingSession
from app.daos.base_dao import BaseDAO
from sqlalchemy import select
from sqlalchemy.sql import func, desc


class TrainingSessionDAO(BaseDAO[TrainingSession]):
    model = TrainingSession

    @staticmethod
    async def has_any_for_user_summary(user_summary_id: int, session: AsyncSession) -> bool:
        """
        Проверяет, есть ли хотя бы одна тренировка у данного пользователя.
        """
        stmt = (
            select(TrainingSession.id)
            .where(TrainingSession.user_summary_id == user_summary_id)
            .limit(1)
        )
        return await session.scalar(stmt) is not None

    @staticmethod
    async def calculate_session_metrics(summary_id: int, session: AsyncSession) -> tuple[int, float, int]:
        """Пересчитывает количество сессий, средний балл и количество выстрелов для summary."""
        res_sessions = await session.execute(
            select(
                func.count(TrainingSession.id),
                func.avg(TrainingSession.score),
                func.sum(TrainingSession.shot_count)
            ).where(TrainingSession.user_summary_id == summary_id)
        )
        sessions_count, avg_score, shot_count = res_sessions.one_or_none() or (0, 0.0, 0)
        return sessions_count or 0, avg_score or 0.0, shot_count or 0

    @staticmethod
    async def total_sessions(summary_id: int, session: AsyncSession) -> tuple[int, int]:
        """Всего сессий и всего дней тренировок"""
        res = await session.execute(
            select(
                func.count(TrainingSession.id),
                func.count(func.distinct(func.date(TrainingSession.date)))
            ).where(TrainingSession.user_summary_id == summary_id)
        )
        total_sessions, total_days = res.one_or_none() or (0, 0)
        return total_sessions or 0, total_days or 0

    @staticmethod
    async def average_score(summary_id: int, session: AsyncSession) -> float:
        """Средний счёт"""
        avg_score = await session.scalar(
            select(func.avg(TrainingSession.score))
            .where(TrainingSession.user_summary_id == summary_id)
        )
        return float(avg_score or 0.0)

    @staticmethod
    async def total_shots(summary_id: int, session: AsyncSession) -> tuple[int, int]:
        """Всего выстрелов и всего дней тренировок"""
        res = await session.execute(
            select(
                func.sum(TrainingSession.shot_count),
                func.count(func.distinct(func.date(TrainingSession.date)))
            ).where(TrainingSession.user_summary_id == summary_id)
        )
        total_shots, total_days = res.one_or_none() or (0, 0)
        return total_shots or 0, total_days or 0

    @staticmethod
    async def best_session(summary_id: int, session: AsyncSession) -> tuple[float, str | None]:
        """Лучшая сессия"""
        result = await session.execute(
            select(TrainingSession.score, TrainingSession.date)
            .where(TrainingSession.user_summary_id == summary_id)
            .order_by(desc(TrainingSession.score))
            .limit(1)
        )
        row = result.one_or_none()
        if row:
            return row.score, row.date
        return 0.0, None

    @staticmethod
    async def last_session_date(summary_id: int, session: AsyncSession) -> str | None:
        """Последняя тренировка"""
        result = await session.scalar(
            select(func.max(TrainingSession.date))
            .where(TrainingSession.user_summary_id == summary_id)
        )
        return result if result else None
