from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel as SchemaBase, Field
from datetime import datetime
from decimal import Decimal
from app.shared import (
    BillableStatus,
    LeadTypes,
    ActionTypes,
    EngagementLevelTypes,
)


class CustomerBase(SchemaBase):
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)


class CustomerCreate(CustomerBase):
    id: str = Field(primary_key=True)


class Customer(CustomerBase):
    created_at: datetime = Field(default=datetime.now())
    actions: Optional[List["Action"]] = Field(default=[])
    billing_reports: Optional[List["BillingReport"]] = Field(default=[])
    leads: Optional[List["Lead"]] = Field(default=[])

    class Config:
        orm_mode = True


class BillingReportProductAssociation(SchemaBase):
    product_id: str = Field(foreign_key="products.id", nullable=False)
    billing_report_id: str = Field(foreign_key="billing_reports.id")


class BillingReportItem(SchemaBase):
    customer_email: str
    associated_product: str
    lead_type: str
    action_type: str
    engagement_level: str
    amount: float
    duplicate: bool
    status: str


# class BillingReport(BaseModel):
#     customer_id: str
#     total_billed_amount: float
#     total_savings: float
#     items: List[BillingReportItem]


class BillingReportBase(SchemaBase):
    customer_id: str = Field(foreign_key="customers.id", nullable=False)
    # products: Optional[List[BillingReportProductAssociation]] = Field(default=None)


class BillingReportCreate(BillingReportBase):
    billing_date: datetime = Field(default=datetime.now())
    total_billed_amount: Decimal = Field(nullable=False)
    savings_amount: Optional[Decimal] = Field(default=0.0)


class BillingReport(BillingReportBase):
    id: str = Field(primary_key=True)
    items: Optional[List[BillingReportItem]] = Field(default=None)
    product_subtotals: Dict[str, float]

    class Config:
        orm_mode = True


class ActionBase(SchemaBase):
    lead_type: LeadTypes = Field(nullable=False)
    action_type: ActionTypes = Field(nullable=False)
    engagement_level: EngagementLevelTypes = Field(nullable=False)
    customer_id: str = Field(foreign_key="customers.id", nullable=False)
    product_id: str = Field(foreign_key="products.id", nullable=False)


class ActionCreate(ActionBase):
    lead_id: str = Field(foreign_key="leads.id", nullable=False)
    created_at: datetime = Field(nullable=False)


class Action(ActionBase):
    id: UUID = Field(primary_key=True)
    is_duplicate: Optional[bool] = Field(default=None)
    status: Optional[BillableStatus] = Field(
        default=None
    )  # Billed or Not Billed (Duplicate)
    cost_amount: Optional[Decimal] = Field(default=None)
    billing_report_id: Optional[str] = Field(
        foreign_key="billing_reports.id", default=None
    )

    class Config:
        orm_mode = True


class LeadBase(SchemaBase):
    lead_type: LeadTypes = Field(nullable=False)
    customer_id: str = Field(foreign_key="customers.id", nullable=False)
    product_id: str = Field(foreign_key="products.id", nullable=False)


class LeadCreate(LeadBase):
    id: str = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(nullable=False)


class Lead(LeadBase):
    actions: Optional[List[Action]] = Field(default=[])

    class Config:
        orm_mode = True


class ProductBase(SchemaBase):
    name: str = Field(nullable=False)
    description: Optional[str] = Field(nullable=True)


class ProductCreate(ProductBase):
    id: str = Field(primary_key=True, nullable=False)


class Product(ProductBase):
    created_at: datetime = Field(default=datetime.now())
    leads: Optional[List[Lead]] = Field(default=[])
    actions: Optional[List["Action"]] = Field(default=[])

    class Config:
        orm_mode = True
