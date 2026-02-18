import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item import ItemService


@pytest.fixture
def service(db_session: AsyncSession) -> ItemService:
    return ItemService(ItemRepository(db_session))


async def test_create(service: ItemService):
    data = ItemCreate(name="Test", price=9.99)
    item = await service.create(data)
    assert item.name == "Test"
    assert item.price == 9.99


async def test_get(service: ItemService):
    data = ItemCreate(name="Test", price=5.0)
    created = await service.create(data)
    found = await service.get(created.id)
    assert found is not None
    assert found.id == created.id


async def test_get_not_found(service: ItemService):
    result = await service.get(999)
    assert result is None


async def test_list(service: ItemService):
    await service.create(ItemCreate(name="A", price=1.0))
    await service.create(ItemCreate(name="B", price=2.0))
    items = await service.list()
    assert len(items) == 2


async def test_update(service: ItemService):
    created = await service.create(ItemCreate(name="Old", price=1.0))
    updated = await service.update(created.id, ItemUpdate(name="New"))
    assert updated is not None
    assert updated.name == "New"


async def test_update_not_found(service: ItemService):
    result = await service.update(999, ItemUpdate(name="X"))
    assert result is None


async def test_delete(service: ItemService):
    created = await service.create(ItemCreate(name="Del", price=1.0))
    assert await service.delete(created.id) is True


async def test_delete_not_found(service: ItemService):
    assert await service.delete(999) is False
