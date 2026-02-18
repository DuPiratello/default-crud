from typing import Generic, TypeVar

from pydantic import BaseModel

from app.repositories.base import BaseRepository

T = TypeVar("T")
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


# Generic service with full CRUD - extend for specific business logic
class BaseService(Generic[T, CreateSchema, UpdateSchema]):
    def __init__(self, repository: BaseRepository[T]) -> None:
        self._repository = repository

    async def get(self, entity_id: int) -> T | None:
        return await self._repository.get_by_id(entity_id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[T]:
        return await self._repository.get_all(skip, limit)

    async def create(self, data: CreateSchema) -> T:
        return await self._repository.create(data.model_dump())

    async def update(self, entity_id: int, data: UpdateSchema) -> T | None:
        return await self._repository.update(
            entity_id, data.model_dump(exclude_unset=True)
        )

    async def delete(self, entity_id: int) -> bool:
        return await self._repository.delete(entity_id)
