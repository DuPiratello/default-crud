from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


# ISP: Interface segregada para operações de leitura
@runtime_checkable
class IReadRepository(Protocol[T]):
    async def get_by_id(self, entity_id: int) -> T | None: ...
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]: ...
    async def count(self) -> int: ...


# ISP: Interface segregada para operações de escrita
@runtime_checkable
class IWriteRepository(Protocol[T]):
    async def create(self, data: dict) -> T: ...
    async def update(self, entity_id: int, data: dict) -> T | None: ...
    async def delete(self, entity_id: int) -> bool: ...


# Interface completa que combina leitura e escrita
@runtime_checkable
class IRepository(IReadRepository[T], IWriteRepository[T], Protocol[T]):
    pass
