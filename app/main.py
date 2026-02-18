from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import v1_router
from app.config import settings
from app.core.exceptions import global_exception_handler
from app.db.base import Base
from app.db.session import engine

STATIC_DIR = Path(__file__).parent / "static"


# Creates tables on startup, disposes engine on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_exception_handler(Exception, global_exception_handler)
app.include_router(v1_router)
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
