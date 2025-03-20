from typing import Annotated
import random
from fastapi import Depends, HTTPException
from fastapi_utils.tasks import repeat_every
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from alembic import context, command
from faker import Faker

from alembic.config import Config
from app.config import settings
import logging
import asyncpg

from app.models import ModelBase
from app.shared import LeadTypes, ActionTypes, EngagementLevelTypes
from app.models import Customer, Product, Lead, Action, BillingReport


async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session: AsyncSession = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def check_database_status():
    logging.info("Checking database status...")
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(ModelBase.metadata.create_all)
        logging.info("Database is up and running.")
    except SQLAlchemyError as e:
        logging.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection error")


async def drop_and_create_tables():
    if settings.ENVIRONMENT != "development":
        logging.info(
            "Skipping drop and create tables because the environment is not development."
        )
        return

    async with async_engine.begin() as conn:
        logging.info("Dropping existing database tables...")
        await conn.run_sync(ModelBase.metadata.drop_all)
        logging.info("Database tables dropped.")
        logging.info("Creating database tables...")
        await conn.run_sync(ModelBase.metadata.create_all)
        logging.info("Database tables created.")


async def run_migrations():
    logging.info("Running migrations...")
    alembic_cfg = context.config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logging.info("Migrations applied.")


async def seed_database(session: AsyncSession):
    # Seed the database ONLY if not already seeded
    async with get_async_session() as session:
        logging.info("Checking if database is seeded...")
        # Check if there's any data in key tables
        result1 = await session.execute(sa.select(Customer).limit(1))
        customer = result.scalar_one_or_none()
        result2 = await session.execute(sa.select(Product).limit(1))
        product = result2.scalar_one_or_none()
        result3 = await session.execute(sa.select(Lead).limit(1))
        lead = result3.scalar_one_or_none()
        result4 = await session.execute(sa.select(Action).limit(1))
        action = result4.scalar_one_or_none()
        # result5 = await session.execute(sa.select(BillingReport).limit(1))
        # billing_report = result5.scalar_one_or_none()

        if not all([customer, product, lead, action]):
            logging.info("Seeding database...")
            fake = Faker()
            lead_types = list(LeadTypes)
            action_types = list(ActionTypes)
            engagement_types = list(EngagementLevelTypes)

            try:
                for _ in range(10):
                    customer = Customer(name=fake.name, email=fake.email)
                    session.add(customer)
                    session.commit()

                    product = Product(name=fake.name, description=fake.text())
                    session.add(product)
                    session.commit()

                    # Create a lead and action
                    lead = Lead(
                        customer_id=customer.id,
                        product_id=product.id,
                        lead_type=random.choice(lead_types),
                        created_at=fake.date_time(),
                    )
                    session.add(lead)
                    await session.commit()

                    for _ in range(3):
                        action = Action(
                            lead_id=lead.id,
                            customer_id=customer.id,
                            product_id=product.id,
                            lead_type=lead.lead_type,
                            action_type=random.choice(action_types),
                            engagement_type=random.choice(engagement_types),
                            created_at=fake.date_time(),
                        )
                        session.add(action)
                        await session.commit()

                logging.info("Database seeded successfully.")
            except SQLAlchemyError as e:
                logging.error(f"Error seeding database: {str(e)}")
                await session.rollback()
                raise HTTPException(status_code=500, detail="Error seeding database")
        else:
            logging.info("Database already seeded.")
