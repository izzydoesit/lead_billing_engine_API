import pytest
from pydantic import ValidationError
from app.schemas import LeadCreate, BillingReportSchema


def test_lead_create_schema():
    # Valid data
    lead_data = {
        "lead_type": "STANDARD",
        "customer_id": str(uuid4()),
        "product_id": str(uuid4()),
    }
    lead = LeadCreate(**lead_data)
    assert lead.lead_type == "STANDARD"

    # Invalid data
    with pytest.raises(ValidationError):
        LeadCreate(lead_type="INVALID")


def test_billing_report_schema():
    report_data = {
        "id": str(uuid4()),
        "customer_id": str(uuid4()),
        "total_billed_amount": 100.0,
        "items": [],
        "product_subtotals": {"Product A": 50.0, "Product B": 50.0},
    }
    report = BillingReportSchema(**report_data)
    assert report.total_billed_amount == 100.0
