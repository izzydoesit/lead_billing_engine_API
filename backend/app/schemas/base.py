from typing import List, Optional
from pydantic import BaseModel as SchemaBase, Field
from datetime import datetime
from decimal import Decimal
from app.shared.billing_lead_types import (
    BillableStatus,
    LeadSources,
    LeadActions,
    LeadQuality,
)


class CustomerBase(SchemaBase):
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)


class CustomerCreate(CustomerBase):
    id: str = Field(primary_key=True)


class Customer(CustomerBase):
    created_at: datetime = Field(default=datetime.now())

    class Config:
        from_attributes = True


class BillingReportProductAssociation(SchemaBase):
    product_id: str = Field(foreign_key="products.id", nullable=False)
    billing_report_id: str = Field(foreign_key="billing_reports.id")


class BillingReportBase(SchemaBase):
    customer_id: str = Field(foreign_key="customers.id", nullable=False)
    products: Optional[List[BillingReportProductAssociation]] = Field(default=None)


class BillingReportCreate(BillingReportBase):
    billing_date: datetime = Field(default=datetime.now())
    total_amount: Decimal = Field(nullable=False)
    savings_amount: Optional[Decimal] = Field(default=0.0)


class BillingReport(BillingReportBase):
    id: str = Field(primary_key=True)

    class Config:
        from_attributes = True


class ProductBase(SchemaBase):
    name: str = Field(nullable=False)
    description: Optional[str] = Field(nullable=True)


class ProductCreate(ProductBase):
    id: str = Field(primary_key=True, nullable=False)


class Product(ProductBase):
    billing_report_id: str = Field(foreign_key="billing_reports.id")
    billing_reports: Optional[List[BillingReport]] = Field(default=None)

    class Config:
        from_attributes = True


class ActionBase(SchemaBase):
    lead_type: LeadSources = Field(nullable=False)
    action_type: LeadActions = Field(nullable=False)
    engagement_level: LeadQuality = Field(nullable=False)
    customer_id: str = Field(foreign_key="customers.id", nullable=False)
    product_id: str = Field(foreign_key="products.id", nullable=False)


class ActionCreate(ActionBase):
    lead_id: str = Field(foreign_key="leads.id", nullable=False)
    created_at: datetime = Field(nullable=False)


class Action(ActionBase):
    id: str = Field(primary_key=True)
    is_duplicate: Optional[bool] = Field(default=None)
    status: Optional[BillableStatus] = Field(
        default=None
    )  # Billed or Not Billed (Duplicate)
    cost_amount: Optional[Decimal] = Field(default=None)
    billing_report_id: str = Field(foreign_key="billing_reports.id")

    class Config:
        from_attributes = True


class LeadBase(SchemaBase):
    lead_type: LeadSources = Field(nullable=False)
    customer_id: str = Field(foreign_key="customers.id", nullable=False)
    product_id: str = Field(foreign_key="products.id", nullable=False)


class LeadCreate(LeadBase):
    id: str = Field(primary_key=True, nullable=False)
    created_at: datetime = Field(nullable=False)


class Lead(LeadBase):
    lead_actions: Optional[List[Action]] = Field(default=[])

    class Config:
        from_attributes = True
