from datetime import datetime
from typing import List, Union, Optional
from pydantic import BaseModel, Field


class LeadBase(BaseModel):
    lead_type: str
    customer_id: int
    product_id: int
    created_at: datetime
    # actions: List[ActionBase]


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    id: int = Field(primary_key=True)

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    name: str
    email: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int = Field(primary_key=True)

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str]


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int = Field(primary_key=True)

    class Config:
        from_attributes = True


class ActionBase(BaseModel):
    action_type: str
    lead_type: str
    engagement_level: str
    lead_id: int = Field(foreign_key=True)
    customer_id: int
    product_id: int
    cost_amount: float
    is_duplicate: Optional[bool] = Field(default=None)
    status: Optional[str] = Field(default=None)  # Billed or Not Billed (Duplicate)
    created_at: datetime


class ActionCreate(ActionBase):
    pass


class Action(ActionBase):
    id: int = Field(primary_key=True)

    class Config:
        from_attributes = True


class BillingReportBase(BaseModel):
    billing_date: str
    customer_name: str
    customer_email: str
    customer_id: int
    # lead_actions: List[ActionBase] = []
    total_amount: float
    savings_amount: Optional[float] = 0.0
    created_at: datetime


class BillingReportCreate(BillingReportBase):
    pass


class BillingReport(BillingReportBase):
    id: int = Field(primary_key=True)

    class Config:
        from_attributes = True
