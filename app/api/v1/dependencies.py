from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.item import ItemRepository
from app.services.item import ItemService


# DIP: Dependency providers - swap implementations without changing endpoints
def get_item_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ItemRepository:
    return ItemRepository(session)


def get_item_service(
    repository: Annotated[ItemRepository, Depends(get_item_repository)],
) -> ItemService:
    return ItemService(repository)


# Type aliases for clean endpoint signatures
ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
