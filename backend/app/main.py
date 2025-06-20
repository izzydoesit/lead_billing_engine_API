from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi_utils.tasks import repeat_every
from alembic import context, config
import asyncio
from .config import settings
from .models import ModelBase
from .core.database import (
    async_engine,
    check_database_status,
    drop_and_create_tables,
    seed_database,
    apply_migrations,
)
from .api.endpoints import health
from .api.endpoints import leads
from .api.endpoints import billing_reports


logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="Lead Billing API",
    description="API for processing billing of customer leads",
    version="0.1.0",
)
if settings.ENVIRONMENT == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.DOMAIN],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
app.include_router(health.router, tags=["health"])
app.include_router(leads.router, tags=["leads"])
app.include_router(billing_reports.router, tags=["billing_reports"])


@app.on_event("startup")
async def startup_event():
    logging.info("~~**~~ Running startup event...")
    await check_database_status()
    await drop_and_create_tables()
    # await apply_migrations()
    await seed_database()


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("~~**~~ Running shutdown event...")
    await async_engine.dispose()
    logging.info("~~**~~ Engine disposed.")


@app.get("/")
def read_root():
    return {"Hello": "World"}
