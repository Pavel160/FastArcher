from sqlalchemy.ext.asyncio import AsyncSession
from app.models.shot_data_model import ShotData
from app.daos.base_dao import BaseDAO


class ShotDataDAO(BaseDAO[ShotData]):
    model = ShotData
