import uuid
from sqlalchemy import String, DateTime, Boolean, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from .models import ModelBase
from .lead import Lead
from .customer import Customer
from .product import Product
from app.shared import (
    LeadTypes,
    ActionTypes,
    EngagementLevelTypes,
    BillableStatus,
)


class Action(ModelBase):
    __tablename__ = "actions"
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, index=True, nullable=False
    )
    lead_id: Mapped[str] = mapped_column(
        String, ForeignKey("leads.id"), nullable=False, index=True
    )
    customer_id: Mapped[str] = mapped_column(
        String, ForeignKey("customers.id"), nullable=False, index=True
    )
    product_id: Mapped[str] = mapped_column(
        String, ForeignKey("products.id"), nullable=False, index=True
    )
    billing_report_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("billing_reports.id"), nullable=True, index=True
    )
    lead_type: Mapped[LeadTypes] = mapped_column(Enum(LeadTypes), nullable=False)
    action_type: Mapped[ActionTypes] = mapped_column(Enum(ActionTypes), nullable=False)
    engagement_level: Mapped[EngagementLevelTypes] = mapped_column(
        Enum(EngagementLevelTypes), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )  # comes populated in POST req payload as timestamp, changed name for consistency, no default value
    cost_amount: Mapped[Optional[Numeric]] = mapped_column(Numeric, default=None)
    is_duplicate: Mapped[Optional[bool]] = mapped_column(Boolean, default=None)
    status: Mapped[Optional[BillableStatus]] = mapped_column(
        Enum(BillableStatus), default=None
    )

    lead: Mapped["Lead"] = relationship("Lead", back_populates="actions", lazy="joined")
    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="actions", lazy="joined"
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="actions", lazy="joined"
    )
    billing_report: Mapped["BillingReport"] = relationship(
        "BillingReport", back_populates="actions", lazy="joined"
    )
