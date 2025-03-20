"""Seed database

Revision ID: abb97a063c02
Revises: bfd038240278
Create Date: 2025-03-19 00:27:47.966044

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import faker as fake
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Customer, Product, Lead, Action
import faker as fake

import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

revision = "abb97a063c02"
down_revision = "bfd038240278"
branch_labels = None
depends_on = None


# TODO: figure out if you need to keep this for migration
def check_version(connection):
    # Example check, customize as needed
    result = connection.execute(
        text("SELECT version_num FROM alembic_version")
    ).fetchone()
    if result:
        current_version = result[0]
        logger.info(f"Current DB version: {current_version}")
        if current_version != "bfd038240278":
            raise Exception(
                f"Expected version bfd038240278 but found {current_version}"
            )
    else:
        logger.info("No version found in alembic_version table.")


def upgrade():

    connection = op.get_bind()
    logger.info("Applying seeding database migration to abb97a063c02")
    session = Session(bind=bind)

    customer = Customer(name="John Doe", email="john@example.com")
    session.add(customer)
    session.commit()

    product = Product(name="Sample Product", description=fake.Faker().text())
    session.add(product)
    session.commit()

    lead = Lead(customer_id=customer.id, product_id=product.id, lead_source="online")
    session.add(lead)
    session.commit()

    action = Action(lead_id=lead.id, description="Initial action")
    session.add(action)
    session.commit()

    # try:
    #     check_version(connection)
    #     op.bulk_insert(
    #         "customers",
    #         [
    #             {"id": "123", "name": "Bob Vila", "email": "bob@homeimprovement.com"},
    #             {"id": "customer-134", "name": "Acme Corp", "email": "john@acme.com"},
    #         ],
    #     )
    #     op.bulk_insert(
    #         "products",
    #         [
    #             {"id": "product-483", "name": "Google", "description": "we searchm"},
    #             {
    #                 "id": "product-133",
    #                 "name": "Acme Corp",
    #                 "description": "john@acme.com",
    #             },
    #         ],
    #     )
    #     op.bulk_insert(
    #         "leads",
    #         [
    #             {
    #                 "id": "123",
    #                 "customer_id": "Bob Vila",
    #                 "email": "bob@homeimprovement.com",
    #             },
    #             {"id": "-134", "a": "Acme Corp", "email": "john@acme.com"},
    #         ],
    #     )
    #     op.bulk_insert(
    #         "actions",
    #         [
    #             {"id": "123", "name": "Bob Vila", "email": "bob@homeimprovement.com"},
    #             {"id": "customer-134", "name": "Acme Corp", "email": "john@acme.com"},
    #         ],
    #     )
    #     await session.commit()
    logger.info("Successfully applied seeding database migration to abb97a063c02")
    # except Exception as e:
    #     logger.error(f"Failed to apply seeding database migration to abb97a063c02: {e}")
    #     raise e


def downgrade():
    connection = op.get_bind()
    logger.info("Reverting upgrade to abb97a063c02")
    session = Session(bind=bind)
    try:
        # session.query(BillingReport).delete()
        session.query(Action).delete()
        session.query(Lead).delete()
        session.query(Product).delete()
        session.query(Customer).delete()
        session.commit()
        logger.info("Successfully reverted upgrade to abb97a063c02")
    except Exception as e:
        logger.error(f"Failed to revert upgrade to abb97a063c02: {e}")
        raise e


def data_upgrades():

    users_table = table("users", column("id", Integer), column("name", String))
    op.bulk_insert(users_table, [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])


def data_downgrades():
    pass
