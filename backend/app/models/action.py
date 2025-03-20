from sqlalchemy import String, DateTime, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from .models import ModelBase
from .lead import Lead
from .customer import Customer
from .product import Product
from app.shared.billing_lead_types import (
    LeadSources,
    LeadActions,
    LeadQuality,
    BillableStatus,
)


class Action(ModelBase):
    __tablename__ = "actions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    lead_id: Mapped[str] = mapped_column(
        ForeignKey("leads.id"), nullable=False, index=True
    )
    customer_id: Mapped[str] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True
    )
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"), nullable=False, index=True
    )
    lead_type: Mapped[LeadSources] = mapped_column(nullable=False)
    action_type: Mapped[LeadActions] = mapped_column(nullable=False)
    engagement_level: Mapped[LeadQuality] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )  # comes populated in POST req payload as timestamp, changed name for consistency, no default value
    cost_amount: Mapped[Optional[Numeric]] = mapped_column(Numeric, default=None)
    is_duplicate: Mapped[Optional[bool]] = mapped_column(Boolean, default=None)
    status: Mapped[Optional[BillableStatus]] = mapped_column(default=None)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="actions")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="actions")
    product: Mapped["Product"] = relationship("Product", back_populates="actions")
    billing_report: Mapped["BillingReport"] = relationship(
        "BillingReport", back_populates="actions"
    )
