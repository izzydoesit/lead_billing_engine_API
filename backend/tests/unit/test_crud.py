import pytest
from app.crud.leads_service import save_lead_in_database, save_action_in_database
from app.crud import calculate_action_value


async def test_save_lead(test_session, test_customer, test_product):
    lead_data = {
        "lead_type": "STANDARD",
        "customer_id": test_customer.id,
        "product_id": test_product.id,
    }

    lead = await save_lead_in_database(test_session, lead_data)
    assert lead.customer_id == test_customer.id
    assert lead.lead_type == "STANDARD"


def test_calculate_action_value():
    value = calculate_action_value("STANDARD", "EMAIL", "HIGH")
    assert value == 5.0
