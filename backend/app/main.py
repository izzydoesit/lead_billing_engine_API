from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic import context, command
import asyncio
from .models import ModelBase
from .database import async_engine, drop_and_create_tables
from .api.endpoints import health
from .api.endpoints import leads
from contextlib import asynccontextmanager

# from .api.endpoints import billing_reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
        await conn.run_sync(ModelBase.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Lead Billing API",
    description="API for processing billing of customer leads",
    version="0.1.0",
)
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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


@app.on_event("shutdown")
async def shutdown_event():
    # You could add shutdown events here
    pass


@app.get("/")
def read_root():
    return {"Hello": "World"}
