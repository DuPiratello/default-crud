from app.models.item import Item
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.base import BaseService


# Item-specific service - add custom business logic here
class ItemService(BaseService[Item, ItemCreate, ItemUpdate]):
    def __init__(self, repository: ItemRepository) -> None:
        super().__init__(repository)
