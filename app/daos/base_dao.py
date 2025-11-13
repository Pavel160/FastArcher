from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel

T = TypeVar("T")  # SQLAlchemy модель
PK = int  # Тип первичного ключа

class BaseDAO(Generic[T]):
    """
    Базовый класс Data Access Object (DAO) для реализации общих
    асинхронных CRUD-операций с любой моделью SQLAlchemy.
    """
    model: Type[T]

    @classmethod
    async def create(cls, session: AsyncSession, schema: BaseModel) -> T:
        """Создает новый объект модели из Pydantic-схемы."""
        obj = cls.model(**schema.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def get(cls, session: AsyncSession, obj_id: PK) -> Optional[T]:
        """Получает объект модели по первичному ключу (id)."""
        stmt = select(cls.model).where(cls.model.id == obj_id)
        return await session.scalar(stmt)

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[T]:
        """Получает все объекты модели."""
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def update(cls, session: AsyncSession, obj_id: PK, schema: BaseModel) -> Optional[T]:
        """Обновляет объект модели по id данными из Pydantic-схемы."""
        values = schema.model_dump(exclude_unset=True)
        stmt = (
            update(cls.model)
            .where(cls.model.id == obj_id)
            .values(**values)
        )
        await session.execute(stmt)
        await session.commit()

        return await cls.get(session, obj_id)

    @classmethod
    async def delete(cls, session: AsyncSession, obj_id: PK) -> bool:
        """Удаляет объект модели по id."""
        result = await session.execute(
            delete(cls.model).where(cls.model.id == obj_id)
        )
        await session.commit()
        return result.rowcount > 0

    @classmethod
    async def filter(cls, session: AsyncSession, **filters) -> List[T]:
        """Фильтрует объекты модели по заданным атрибутам"""
        stmt = select(cls.model).filter_by(**filters)
        result = await session.execute(stmt)
        return result.scalars().all()
