import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # print(f"lifespan loop ID: {id(asyncio.get_running_loop())}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
