import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.repositories.base import BaseRepository


@pytest.fixture
def repository(db_session: AsyncSession) -> BaseRepository[Item]:
    return BaseRepository(db_session, Item)


async def test_create(repository: BaseRepository[Item], db_session: AsyncSession):
    item = await repository.create({"name": "Test", "price": 9.99})
    assert item.id is not None
    assert item.name == "Test"
    assert item.price == 9.99


async def test_get_by_id(repository: BaseRepository[Item], db_session: AsyncSession):
    created = await repository.create({"name": "Test", "price": 5.0})
    found = await repository.get_by_id(created.id)
    assert found is not None
    assert found.id == created.id


async def test_get_by_id_not_found(repository: BaseRepository[Item]):
    result = await repository.get_by_id(999)
    assert result is None


async def test_get_all(repository: BaseRepository[Item], db_session: AsyncSession):
    await repository.create({"name": "A", "price": 1.0})
    await repository.create({"name": "B", "price": 2.0})
    items = await repository.get_all()
    assert len(items) == 2


async def test_get_all_pagination(
    repository: BaseRepository[Item], db_session: AsyncSession
):
    for i in range(5):
        await repository.create({"name": f"Item {i}", "price": float(i)})
    page = await repository.get_all(skip=2, limit=2)
    assert len(page) == 2


async def test_count(repository: BaseRepository[Item], db_session: AsyncSession):
    assert await repository.count() == 0
    await repository.create({"name": "A", "price": 1.0})
    assert await repository.count() == 1


async def test_update(repository: BaseRepository[Item], db_session: AsyncSession):
    created = await repository.create({"name": "Old", "price": 1.0})
    updated = await repository.update(created.id, {"name": "New"})
    assert updated is not None
    assert updated.name == "New"


async def test_update_not_found(repository: BaseRepository[Item]):
    result = await repository.update(999, {"name": "X"})
    assert result is None


async def test_delete(repository: BaseRepository[Item], db_session: AsyncSession):
    created = await repository.create({"name": "Del", "price": 1.0})
    assert await repository.delete(created.id) is True
    assert await repository.get_by_id(created.id) is None


async def test_delete_not_found(repository: BaseRepository[Item]):
    assert await repository.delete(999) is False
