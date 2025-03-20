from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import asyncpg
from .models import ModelBase
from .config import settings

DATABASE_URL = settings.DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session: AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def drop_and_create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)
