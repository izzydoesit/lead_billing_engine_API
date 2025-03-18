from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from billing_lead_types import LeadTypes, ActionTypes, EngagementLevelTypes


class CustomerBase(BaseModel):
    name: str
    email: str


class CustomerCreate(CustomerBase):
    id: str = Field(primary_key=True)


class Customer(CustomerBase):

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str]


class ProductCreate(ProductBase):
    id: str = Field(primary_key=True)


class Product(ProductBase):

    class Config:
        from_attributes = True


class ActionBase(BaseModel):
    action_type: ActionTypes = Field(nullable=False)
    engagement_level: EngagementLevelTypes = Field(nullable=False)
    timestamp: datetime = Field(nullable=False)


class ActionCreate(ActionBase):
    lead_id: str = Field(foreign_key="leads.id")
    lead_type: LeadTypes = Field(foreign_key="leads.lead_type")
    customer_id: str = Field(foreign_key="customers.id")
    product_id: str = Field(foreign_key="products.id")


class Action(ActionBase):
    id: int = Field(primary_key=True)
    is_duplicate: Optional[bool] = Field(default=None)
    status: Optional[str] = Field(default=None)  # Billed or Not Billed (Duplicate)
    cost_amount: Optional[float] = Field(default=None)

    class Config:
        from_attributes = True


class LeadBase(BaseModel):
    customer_id: str = Field(foreign_key="customers.id")
    product_id: str = Field(foreign_key="products.id")
    lead_type: LeadTypes = Field(nullable=False)


class LeadCreate(LeadBase):
    id: str = Field(primary_key=True)
    actions: List[Action] = []
    created_at: datetime = Field(nullable=False)


class Lead(LeadBase):

    class Config:
        from_attributes = True


class BillingReportBase(BaseModel):
    customer_name: str = Field(foreign_key="customers.name")
    customer_email: str = Field(foreign_key="customers.email")
    reported_actions: List[Action] = []


class BillingReportCreate(BillingReportBase):
    customer_id: str = Field(foreign_key="customers.id")


class BillingReport(BillingReportBase):
    id: int = Field(primary_key=True)
    billing_date: datetime = Field(nullable=False, default=datetime.now())
    total_amount: float = Field(nullable=False)
    savings_amount: Optional[float] = 0.0

    class Config:
        from_attributes = True
