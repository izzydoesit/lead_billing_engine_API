import pytest
from app.models import Lead, Customer, Product, Action
from sqlalchemy.exc import IntegrityError


async def test_customer_model(test_session):
    customer = Customer(id=str(uuid4()), name="Test Customer", email="test@example.com")
    test_session.add(customer)
    await test_session.commit()

    result = await test_session.get(Customer, customer.id)
    assert result.name == "Test Customer"


async def test_lead_model_relationships(test_session, test_customer, test_product):
    lead = Lead(
        id=str(uuid4()),
        lead_type="STANDARD",
        customer_id=test_customer.id,
        product_id=test_product.id,
    )
    test_session.add(lead)
    await test_session.commit()

    result = await test_session.get(Lead, lead.id)
    assert result.customer.name == "Test Customer"
    assert result.product.name == "Test Product"
