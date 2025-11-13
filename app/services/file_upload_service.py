import asyncio
from app.daos.training_session_dao import TrainingSessionDAO
from app.services.utils.parses_file import ParsesService
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.daos.user_dao import UserDAO
from app.daos.user_summaries_dao import UserSummaryDAO
from app.models.training_session_model import TrainingSession
from app.models.shot_data_model import ShotData
from app.services.utils.user_summary_service import update_user_summary


class UploadService:
    """Сервис загрузки CSV."""
    @staticmethod
    async def process_csv_upload(telegram_id: int, file: UploadFile, db: AsyncSession) -> list[dict]:
        """Основной метод обработки загруженного CSV-файла."""
        content = await file.read()
        lines = ParsesService.clean_file_content(content)

        user = await UserDAO.get_active_user_by_telegram_id(telegram_id, db)
        if not user:
            raise ValueError("Пользователь не найден. Пожалуйста, зарегистрируйтесь.")
        if not user.is_active:
            raise ValueError("Вы не вошли в систему. Сначала выполните вход.")

        csv_username = ParsesService.extract_username_from_header(content)
        if csv_username and csv_username.lower() != user.username.lower():
            raise ValueError(
            f"Имя пользователя в файле ({csv_username}) не совпадает с вашим ({user.username})."
            "Проверьте, что вы загружаете свой файл."
        )

        summary = await UserSummaryDAO.get_or_create_summary(user.id, user.username, db)
        user_summary_id = summary.id
        status_messages = []

        training_rows_raw = await asyncio.to_thread(
            ParsesService.parse_session_data, lines, user_summary_id
            )
        shot_rows_raw = await asyncio.to_thread(
            ParsesService.parse_shot_data, lines
            )
        if shot_rows_raw and not training_rows_raw:
            has_sessions_before = await TrainingSessionDAO.has_any_for_user_summary(summary.id, db)
            if not has_sessions_before:
                raise ValueError("Сначала загрузите файл **Sessions** а затем **Shots**.")

        added_sessions = 0
            #  ОБРАБОТКА TRAINING_SESSION
        if training_rows_raw:
            ready_sessions = await asyncio.to_thread(ParsesService.clean_and_filter_rows,
                TrainingSession, training_rows_raw)

            if ready_sessions:
                insert_stmt = pg_insert(TrainingSession).values(ready_sessions)
                insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['id'])
                result = await db.execute(insert_stmt)

                added_sessions = result.rowcount
                if added_sessions > 0:
                    await update_user_summary(user.username, db, part="sessions")
                    status_messages.append(f"🎯 TrainingSession: {added_sessions} новых")
                else:
                    status_messages.append("⚠️ TrainingSession: все строки были дубликатами")

        #  ОБРАБОТКА SHOT_DATA
        if shot_rows_raw:
            ready_shots = await asyncio.to_thread(ParsesService.clean_and_filter_rows,
                ShotData, shot_rows_raw)

            if ready_shots:
                insert_stmt = pg_insert(ShotData).values(ready_shots)
                insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['time_stamp'])
                result = await db.execute(insert_stmt)

                added_shots = result.rowcount
                if added_shots > 0:
                    status_messages.append(f"🏹 ShotData: {added_shots} новых")
                else:
                    status_messages.append("⚠️ ShotData: все строки были дубликатами")

        await db.commit()

        if status_messages:
            return {"message": "✅ " + ", ".join(status_messages)}
        else:
            return {"message": "⚠️ Не удалось определить данные для загрузки"}
