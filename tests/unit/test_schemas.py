import pytest
from pydantic import ValidationError

from app.schemas.item import ItemCreate, ItemUpdate


def test_item_create_valid():
    item = ItemCreate(name="Test", price=9.99)
    assert item.name == "Test"
    assert item.price == 9.99
    assert item.is_active is True


def test_item_create_missing_name():
    with pytest.raises(ValidationError):
        ItemCreate(price=9.99)


def test_item_create_missing_price():
    with pytest.raises(ValidationError):
        ItemCreate(name="Test")


def test_item_create_negative_price():
    with pytest.raises(ValidationError):
        ItemCreate(name="Test", price=-1.0)


def test_item_create_zero_price():
    with pytest.raises(ValidationError):
        ItemCreate(name="Test", price=0)


def test_item_create_empty_name():
    with pytest.raises(ValidationError):
        ItemCreate(name="", price=9.99)


def test_item_update_partial():
    update = ItemUpdate(name="New Name")
    assert update.name == "New Name"
    assert update.price is None
    assert update.is_active is None


def test_item_update_all_none():
    update = ItemUpdate()
    assert update.name is None
    assert update.price is None
