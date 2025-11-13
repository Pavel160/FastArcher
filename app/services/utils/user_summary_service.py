from typing import Optional
from app.daos.shot_data_dao import ShotDataDAO
from app.daos.training_session_dao import TrainingSessionDAO
from sqlalchemy.ext.asyncio import AsyncSession
from app.daos.user_dao import UserDAO
from app.daos.user_summaries_dao import UserSummaryDAO


async def update_user_summary(
    username: str, db: AsyncSession, part: Optional[str] = None
):
    """
    Обновляет статистику тренировки (UserSummary) по указанному имени пользователя.
    """

    #  Находим пользователя
    user = await UserDAO.get_by_username(username, db)
    if not user:
        return

    #  Находим или создаём summary
    summary = await UserSummaryDAO.get_or_create_summary(user.id, user.username, db)

    #  Пересчитываем количество сессий и средний балл и количество выстрелов
    if part in (None, "sessions"):
        sessions_count, avg_score, shot_count = (
            await TrainingSessionDAO.calculate_session_metrics(summary.id, db)
        )

        summary.sessions = sessions_count
        summary.average_score = avg_score
        summary.shots = shot_count
