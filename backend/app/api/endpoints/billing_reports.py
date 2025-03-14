from fastapi import APIRouter

router = APIRouter()

@router.get("/billing-reports")
def read_billing_reports():
    return {"billing_reports": [{ "report_id": "1234" }]}