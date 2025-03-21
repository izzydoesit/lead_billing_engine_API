"""Seed database

Revision ID: abb97a063c02
Revises: bfd038240278
Create Date: 2025-03-19 00:27:47.966044

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Customer, Product, Lead, Action
from faker import Faker
import random
import logging
from app.shared import LeadTypes, ActionTypes, EngagementLevelTypes

logger = logging.getLogger(__name__)

revision = "abb97a063c02"
down_revision = "bfd038240278"
branch_labels = None
depends_on = None

# Enums
leadtypes_enum = postgresql.ENUM(
    "WEBSITE_VISIT",
    "SOCIAL_MEDIA",
    "EMAIL_CAMPAIGN",
    "REFERRAL",
    "EVENT",
    "WEBINAR",
    "DEMO_REQUEST",
    "TRADE_SHOW",
    "CONFERENCE",
    "NEWSLETTER",
    "FEEDBACK",
    name="leadtypes",
)

actiontypes_enum = postgresql.ENUM(
    "VISIT",
    "DOWNLOAD",
    "FORM_SUBMIT",
    "PURCHASE",
    "LIKE",
    "FOLLOW",
    "SHARE",
    "COMMENT",
    "REPOST",
    "OPEN",
    "CLICK",
    "UNSUBSCRIBE",
    "SIGNUP",
    "REGISTER",
    "ATTEND",
    "FOLLOW_UP",
    "ATTENDANCE",
    "SUBMISSION",
    name="actiontypes",
)

engagementleveltypes_enum = postgresql.ENUM(
    "LOW", "MEDIUM", "HIGH", name="engagementleveltypes"
)


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
    session = Session(bind=connection)

    fake = Faker()

    try:
        logger.info("** Creating enums...")
        # Create enums
        leadtypes_enum.create(op.get_bind())
        actiontypes_enum.create(op.get_bind())
        engagementleveltypes_enum.create(op.get_bind())
        logger.info("** Seeding database...")

        # Seed Customers and Products
        customers = []
        products = []
        for _ in range(10):
            customer = Customer(id=fake.uuid4(), name=fake.name(), email=fake.email())
            session.add(customer)
            customers.append(customer)

            product = Product(
                id=fake.uuid4(), name=fake.word(), description=fake.text()
            )
            session.add(product)
            products.append(product)

        session.commit()

        # Seed Leads and Actions
        for customer in customers:
            for product in products:
                lead = Lead(
                    id=fake.uuid4(),
                    customer_id=customer.id,
                    product_id=product.id,
                    lead_type=fake.random_element(list(LeadTypes)).name,
                    created_at=fake.date_time_this_decade(),
                )
                session.add(lead)
                session.commit()

                for _ in range(3):
                    action = Action(
                        id=fake.uuid4(),
                        lead_id=lead.id,
                        customer_id=customer.id,
                        product_id=product.id,
                        lead_type=lead.lead_type,
                        action_type=fake.random_element(list(ActionTypes)).name,
                        engagement_level=fake.random_element(
                            list(EngagementLevelTypes)
                        ).name,
                        created_at=fake.date_time_this_decade(),
                    )
                    lead.actions.append(action)
                    customer.actions.append(action)
                    product.actions.append(action)
                    session.add(action)
                    session.commit()

        logger.info("Successfully applied seeding database migration to abb97a063c02")
    except Exception as e:
        logger.error(
            f"Failed to apply seeding database migration to abb97a063c02: {str(e)}"
        )
        session.rollback()
        raise e
    finally:
        session.close()


def downgrade():
    connection = op.get_bind()
    logger.info("Reverting upgrade to abb97a063c02")
    session = Session(bind=bind)
    try:
        session.query(Action).delete()
        session.query(Lead).delete()
        session.query(Product).delete()
        session.query(Customer).delete()
        session.commit()
        logger.info("Successfully reverted upgrade to abb97a063c02")
    except Exception as e:
        logger.error(f"Failed to revert upgrade to abb97a063c02: {e}")
        raise e
    finally:
        session.close()
