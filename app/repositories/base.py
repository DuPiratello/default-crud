from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

T = TypeVar("T", bound=Base)


# Generic repository with full CRUD - extend for specific entities
class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self._session = session
        self._model = model

    async def get_by_id(self, entity_id: int) -> T | None:
        return await self._session.get(self._model, entity_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        query = select(self._model).offset(skip).limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def count(self) -> int:
        query = select(func.count(self._model.id))
        result = await self._session.execute(query)
        return result.scalar_one()

    async def create(self, data: dict) -> T:
        entity = self._model(**data)
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def update(self, entity_id: int, data: dict) -> T | None:
        entity = await self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(entity, key, value)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity_id: int) -> bool:
        entity = await self.get_by_id(entity_id)
        if not entity:
            return False
        await self._session.delete(entity)
        await self._session.flush()
        return True
