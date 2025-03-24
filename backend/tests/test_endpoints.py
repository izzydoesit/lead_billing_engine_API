import pytest
from httpx import AsyncClient
from fastapi import status


async def test_create_lead(test_client, test_customer, test_product):
    lead_data = {
        "lead_type": "STANDARD",
        "customer_id": test_customer.id,
        "product_id": test_product.id,
    }

    response = await test_client.post("/leads", json=lead_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["customer_id"] == test_customer.id


async def test_get_billing_report(test_client, test_customer):
    response = await test_client.get(f"/billingReports?customer_id={test_customer.id}")
    assert response.status_code == status.HTTP_200_OK
    assert "items" in response.json()
    assert "total_billed_amount" in response.json()
