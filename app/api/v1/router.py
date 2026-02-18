from fastapi import APIRouter

from app.api.v1.endpoints import items

# V1 router - register all endpoint routers here
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(items.router)
