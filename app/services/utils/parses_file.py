import io
import pandas as pd
from datetime import datetime
from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect, Integer, Float, DateTime


class ParsesService:
    """Сервис обработки CSV. """

    @staticmethod
    def clean_file_content(content: bytes) -> list[str]:
        """Чтение и базовая очистка файла (пропуск первых 4 строк)."""
        text = content.decode("utf-8")
        lines = text.splitlines()
        if len(lines) > 4:
            lines = lines[4:]
        return lines

    @staticmethod
    def extract_username_from_header(content: bytes) -> Optional[str]:
        """Извлекает имя пользователя из CSV, даже если строка не содержит 'username'."""
        text = content.decode("utf-8")
        lines = text.splitlines()

        for i, line in enumerate(lines[:4]):
            clean_line = line.strip()
            if clean_line.lower().startswith("username"):
                df = pd.read_csv(
                    io.StringIO(clean_line),
                    header=None,
                    sep=',',
                    engine="python"
                )
                if df.shape[1] > 1:
                    raw_username = df.iloc[0, 1]

                    if pd.isna(raw_username):
                        return None
                    username = str(raw_username).strip().strip('"')
                    return username
        return None

    @staticmethod
    def parse_session_data(lines: list[str], user_summary_id: int) -> Optional[list[dict]]:
        """Парсит TrainingSession, форматирует колонки с Pandas."""
        df = None

        for i, line in enumerate(lines):
            if line.startswith(("ID,", "ID\t")):
                df = pd.read_csv(
                    io.StringIO("\n".join(lines[i:])),
                    sep=None,
                    engine='python',
                    keep_default_na=True
                )
                break

        if df is None:
            return None

        #  Нормализуем имена колонок
        df.columns = (
            df.columns.str.strip()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
            .str.lower()
        )

        #  Разделяем комбинированные колонки
        split_columns = {
            "cant/pitch": ["cant", "pitch"],
            "d_loop/holding_weight/peep_height": ["d_loop", "holding_weight", "peep_height"],
            "draw_weight/draw_length": ["draw_weight", "draw_length"],
            "front_stabilizer_weight/length": ["front_stabilizer_weight", "front_stabilizer_length"],
            "rear_left_stabilizer_weight/length": ["rear_left_stabilizer_weight", "rear_left_stabilizer_length"],
            "rear_right_stabilizer_weight/length": ["rear_right_stabilizer_weight", "rear_right_stabilizer_length"]
        }

        for col, new_cols in split_columns.items():
            if col in df.columns:
                df[new_cols] = df[col].astype(str).str.split("/", expand=True)
                df.drop(columns=[col], inplace=True)

        df["user_summary_id"] = user_summary_id
        return df.to_dict(orient="records")

    @staticmethod
    def parse_shot_data(lines: list[str]) -> Optional[list[dict]]:
        """Парсит ShotData, форматирует колонки для модели."""
        df = None

        for i, line in enumerate(lines):
            if line.startswith(("Session ID", "Session ID\t")):
                df = pd.read_csv(
                    io.StringIO("\n".join(lines[i:])),
                    sep=None,
                    engine="python",
                    keep_default_na=True
                )
                break

        if df is None:
            return None

        #  Нормализация имён колонок
        df.columns = (
        df.columns.str.strip()
                  .str.replace("-", "_", regex=False)
                  .str.replace("(", "", regex=False)
                  .str.replace(")", "", regex=False)
                  .str.replace(" ", "_", regex=False)
                  .str.lower()
        )

        return df.to_dict(orient="records")

    @staticmethod
    def clean_and_filter_rows(
        model,
        rows: list[dict],
    ) -> List[Any]:
        """Очистка значений, конвертация типов."""

        objects_to_add = []
        mapper = inspect(model)
        model_fields = {c.key: c.type for c in mapper.columns}

        unknown_columns = set()
        for row in rows:
            clean_row = {}

            for key, value in row.items():
                if not key or key not in model_fields:
                    unknown_columns.add(key)
                    continue
                column_type = model_fields[key]

                #  Проверка на "пустые" значения
                if (
                    pd.isna(value)
                    or str(value).strip() in {"", "/", "//", "---"}
                ):
                    clean_row[key] = None
                    continue

                #  Приведение типов
                try:
                    if isinstance(column_type, Integer):
                        clean_row[key] = int(value)
                    elif isinstance(column_type, Float):
                        clean_row[key] = float(value)
                    elif isinstance(column_type, DateTime):
                        clean_row[key] = datetime.fromisoformat(str(value).replace(" UTC", ""))
                    else:
                        clean_row[key] = str(value).strip()
                except (ValueError, TypeError):
                    clean_row[key] = None

            if not clean_row:
                continue

            objects_to_add.append(clean_row)

        #  Если найдены неожиданные колонки — останавливаем процесс и сообщаем
        if unknown_columns:
            raise ValueError(
                f"Обнаружены неизвестные столбцы в CSV для модели {model.__name__}: "
                f"{', '.join(unknown_columns)}"
            )

        return objects_to_add
