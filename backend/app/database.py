from typing import Annotated
from fastapi import Depends
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import IntegrityError
import app.models as models
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session: AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)
# async_engine = create_async_engine(ConnectionString, future=True, echo=True)
# async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


db_dependency = Annotated[
    AsyncSession, Depends(get_async_session)
]  # This is the dependency for FastAPI routes


async def drop_and_create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
