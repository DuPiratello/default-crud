from fastapi import APIRouter, Query, status

from app.api.v1.dependencies import ItemServiceDep
from app.core.exceptions import NotFoundException
from app.schemas.base import PaginatedResponse
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["Items"])


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create item",
    description="Creates a new item with the provided data.",
)
async def create_item(data: ItemCreate, service: ItemServiceDep) -> ItemResponse:
    item = await service.create(data)
    return ItemResponse.model_validate(item)


@router.get(
    "/",
    response_model=PaginatedResponse[ItemResponse],
    summary="List items",
    description="Returns a paginated list of all items.",
)
async def list_items(
    service: ItemServiceDep,
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
) -> PaginatedResponse[ItemResponse]:
    items = await service.list(skip=skip, limit=limit)
    total = await service._repository.count()
    return PaginatedResponse(
        items=[ItemResponse.model_validate(i) for i in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item",
    description="Returns a single item by its ID.",
)
async def get_item(item_id: int, service: ItemServiceDep) -> ItemResponse:
    item = await service.get(item_id)
    if not item:
        raise NotFoundException("Item", item_id)
    return ItemResponse.model_validate(item)


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update item",
    description="Updates an existing item with the provided data.",
)
async def update_item(
    item_id: int, data: ItemUpdate, service: ItemServiceDep
) -> ItemResponse:
    item = await service.update(item_id, data)
    if not item:
        raise NotFoundException("Item", item_id)
    return ItemResponse.model_validate(item)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item",
    description="Permanently removes an item by its ID.",
)
async def delete_item(item_id: int, service: ItemServiceDep) -> None:
    deleted = await service.delete(item_id)
    if not deleted:
        raise NotFoundException("Item", item_id)
