from sqlalchemy.ext.asyncio import AsyncSession
from app.daos.training_session_dao import TrainingSessionDAO
from app.daos.user_summaries_dao import UserSummaryDAO
from typing import Optional


class StatsService:

    @staticmethod
    async def get_total_sessions(user_id: int, db: AsyncSession) -> Optional[dict[str, int]]:
        """Общее количество сессий и дней."""
        summary = await UserSummaryDAO.get_summary_by_user_id(user_id, db)
        if not summary:
            raise ValueError(f"Сводная запись пользователя не найдена для user_id: {user_id}")

        user_summary_id = summary.id
        sessions_count, total_days = await TrainingSessionDAO.total_sessions(user_summary_id, db)
        if sessions_count == 0:
            raise ValueError("Нет записанных тренировочных сессий для этого пользователя.")

        return {
            "total_sessions": sessions_count,
            "total_days": total_days
            }

    @staticmethod
    async def get_average_score(user_id: int, db: AsyncSession) -> Optional[dict[str, float]]:
        """Средний балл."""
        summary = await UserSummaryDAO.get_summary_by_user_id(user_id, db)
        if not summary:
            raise ValueError(f"Сводная запись пользователя не найдена для user_id: {user_id}")

        user_summary_id = summary.id
        avg_score = await TrainingSessionDAO.average_score(user_summary_id, db)
        if not avg_score:
            raise ValueError("Невозможно посчитать средний счёт: нет данных о тренировках.")

        return {"average_score": round(float(avg_score), 2)}

    @staticmethod
    async def get_total_shots(user_id: int, db: AsyncSession) -> Optional[dict[str, int]]:
        """Общее количество выстрелов."""
        summary = await UserSummaryDAO.get_summary_by_user_id(user_id, db)
        if not summary:
            raise ValueError(f"Сводная запись пользователя не найдена для user_id: {user_id}")

        user_summary_id = summary.id
        total_shots, total_days = await TrainingSessionDAO.total_shots(user_summary_id, db)
        if total_shots == 0:
            raise ValueError("Нет данных о выстрелах для этого пользователя.")

        return {
            "total_shots": total_shots,
            "total_days_shots": total_days
        }

    @staticmethod
    async def get_best_session(user_id: int, db: AsyncSession) -> Optional[dict[str, str | float]]:
        """Лучший счёт и дата."""
        summary = await UserSummaryDAO.get_summary_by_user_id(user_id, db)
        if not summary:
            raise ValueError(f"Сводная запись пользователя не найдена для user_id: {user_id}")

        user_summary_id = summary.id
        best_score, best_date = await TrainingSessionDAO.best_session(user_summary_id, db)
        if not best_date:
            raise ValueError("Не найдено ни одной завершённой сессии для лучшего счёта.")

        return {
            "best_score": best_score,
            "date": best_date.isoformat(timespec="seconds")
        }

    @staticmethod
    async def get_last_session_date(user_id: int, db: AsyncSession) -> Optional[dict[str, str]]:
        """Дата последней тренировки."""
        summary = await UserSummaryDAO.get_summary_by_user_id(user_id, db)
        if not summary:
            raise ValueError(f"Сводная запись пользователя не найдена для user_id: {user_id}")

        user_summary_id = summary.id
        last_date = await TrainingSessionDAO.last_session_date(user_summary_id, db)
        if not last_date:
            raise ValueError("Не найдено данных о дате последней тренировки.")

        return {"last_session_date": last_date.isoformat(timespec="seconds")}
