import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.engine import create_async_engine

# Import your models here
from app.models import *

# from app.models.leads_config import LeadsConfig
# from app.models.order_transactions import OrderTransaction

from app.config import settings  # Import settings for the database URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add models here to include them in the migration detection.
# EX: poetry run alembic-dev revision --autogenerate -m "Create leads_configs table"

target_metadata = ModelBase.metadata

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        connectable = create_async_engine(
            settings.DATABASE_URL, poolclass=pool.NullPool, future=True
        )

    if isinstance(connectable, AsyncEngine):
        asyncio.run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()
