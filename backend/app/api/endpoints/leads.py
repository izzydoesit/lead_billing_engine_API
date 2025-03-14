from fastapi import APIRouter

router = APIRouter()

@router.get("/leads")
def read_leads():
    return {"leads": [{ "lead_id": "uuid-1234"}]}

@router.get("/leads/{lead_id}")
def read_lead(lead_id: int, q: Union[str, None] = None):
    return { "id": lead_id, "q": q }

@router.post("/leads")
def write_lead():
    return { "status": "lead successfully created" }