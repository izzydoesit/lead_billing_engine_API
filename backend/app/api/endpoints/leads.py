from typing import List, Union
from fastapi import APIRouter, HTTPException
from database import db_dependency
import models
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

router = APIRouter()

class LeadBase(BaseModel):
    lead_id: Optional[UUID] = Field(default=None, primary_key=True)
    lead_type: str
    customer_id: UUID
    actions: List[models.ActionBase] = []

class ActionBase(BaseModel):
    action_id: UUID
    action_type: str
    lead_type: str
    engagement_level: str
    lead_id: UUID
    customer_id: UUID
    product_id: UUID
    cost_amount: float
    is_duplicate: Optional[bool] = None
    status: Optional[str] = None # Billed or Not Billed (Duplicate)

class CustomerBase(BaseModel):
    customer_id: UUID
    name: str
    email: str

@router.get("/leads/{lead_id}")
async def read_lead(lead_id: int, db: db_dependency):
    result = db.query(models.Leads).filter(models.Leads.lead_id == lead_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result

@router.get("/leads?q={query}")
async def find_leads(db: db_dependency, query: Union[str, None] = None) -> List[LeadBase]:
    if query:
        if query.customer_id and not query.lead_type:
            result = db.query(models.Leads).filter(models.Leads.customer_id == query.customer_id).all()
        elif query.lead_type and not query.customer_id:
            result = db.query(models.Leads).filter(models.Leads.lead_type == query.lead_type).all()
        elif query.customer_id and query.lead_type:
            result = db.query(models.Leads).filter(models.Leads.customer_id == query.customer_id, models.Leads.lead_type == query.lead_type).all()
        else:
            raise HTTPException(status_code=400, detail="Invalid query parameters") 
    else:
        result = db.query(models.Leads).all()

    if result is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result

@router.post("/leads")
async def create_lead(lead: LeadBase, db: db_dependency):
    db_lead = models.Lead(lead_type=lead.lead_type, customer_id=lead.customer_id, product_id=lead.product_id)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    for action in lead.actions:
        db_action = models.Action(**action.dict())
        db.add(db_action)
    db.commit()
    return db_lead
