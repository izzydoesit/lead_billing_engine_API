# app/seed_data.py
"""
Script to seed the database with sample data for development and testing
"""
import logging
import random
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
from fastapi import HTTPException
from app.core.database import SessionLocal
from app.core.database import async_session
from app.models import ModelBase, Customer, Product, Lead, Action
from app.shared import LeadTypes, ActionTypes, EngagementLevelTypes


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_initial_data() -> None:
    async with async_session() as session:
        logging.info("~~**~~ Checking if database is seeded...")
        # Check if there's any data in key tables
        result1 = await session.execute(select(Customer).limit(1))
        customer = result1.scalar_one_or_none()
        result2 = await session.execute(select(Product).limit(1))
        product = result2.scalar_one_or_none()
        result3 = await session.execute(select(Lead).limit(1))
        lead = result3.scalar_one_or_none()
        result4 = await session.execute(select(Action).limit(1))
        action = result4.scalar_one_or_none()

        if not all([customer, product, lead, action]):
            logging.info("~~**~~ Data incomplete. Seeding database...")
            fake = Faker()
            lead_types = list(LeadTypes)
            action_types = list(ActionTypes)
            engagement_types = list(EngagementLevelTypes)

            try:
                for _ in range(10):
                    customer = Customer(
                        id=str(fake.uuid4()), name=fake.name(), email=fake.email()
                    )
                    session.add(customer)
                    await session.commit()

                    product = Product(
                        id=str(fake.uuid4()), name=fake.name(), description=fake.text()
                    )
                    session.add(product)
                    await session.commit()

                    # Create a lead and action
                    lead = Lead(
                        id=str(fake.uuid4()),
                        customer_id=customer.id,
                        product_id=product.id,
                        lead_type=random.choice(lead_types),
                        created_at=fake.date_time(),
                    )
                    session.add(lead)
                    await session.commit()

                    for _ in range(3):
                        action = Action(
                            id=str(fake.uuid4()),
                            lead_id=lead.id,
                            customer_id=customer.id,
                            product_id=product.id,
                            lead_type=lead.lead_type,
                            action_type=random.choice(action_types),
                            engagement_level=random.choice(engagement_types),
                            created_at=fake.date_time(),
                        )
                        session.add(action)
                        await session.commit()

                logging.info("~~**~~ Database seeded successfully.")
            except SQLAlchemyError as e:
                logging.error(f"Error seeding database: {str(e)}")
                await session.rollback()
                raise HTTPException(status_code=500, detail="Error seeding database")
        else:
            logging.info("~~**~~ Database already seeded.")


def main() -> None:
    """Main function to seed all tables"""
    logger.info("Starting database seeding...")

    try:
        seed_initial_data()
        logger.info("Database seeding completed successfully")
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        raise e


if __name__ == "__main__":
    main()
