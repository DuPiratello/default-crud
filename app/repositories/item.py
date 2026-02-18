from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.repositories.base import BaseRepository


# Item-specific repository - add custom queries here
class ItemRepository(BaseRepository[Item]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Item)
