from fastapi import FastAPI
from .models import ModelBase
from .database import async_engine, drop_and_create_tables
from .api.endpoints import health
from .api.endpoints import leads
from alembic import context, command
import asyncio

from contextlib import asynccontextmanager

# from .api.endpoints import billing_reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(health.router, tags=["health"])
app.include_router(leads.router, tags=["leads"])
# app.include_router(billing_reports.router, tags=["billing_reports"])


async def run_migrations():
    alembic_cfg = context.config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@app.on_event("startup")
async def startup_event():
    pass
    # await drop_and_create_tables()
    # await run_migrations()


@app.get("/")
def read_root():
    return {"Hello": "World"}
