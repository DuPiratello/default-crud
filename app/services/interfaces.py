from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")


# ISP: Interface segregada para leitura
@runtime_checkable
class IReadService(Protocol[T]):
    async def get(self, entity_id: int) -> T | None: ...
    async def list(self, skip: int = 0, limit: int = 100) -> list[T]: ...


# ISP: Interface segregada para escrita
@runtime_checkable
class IWriteService(Protocol[T]):
    async def create(self, data: object) -> T: ...
    async def update(self, entity_id: int, data: object) -> T | None: ...
    async def delete(self, entity_id: int) -> bool: ...


# Interface completa que combina leitura e escrita
@runtime_checkable
class IService(IReadService[T], IWriteService[T], Protocol[T]):
    pass
