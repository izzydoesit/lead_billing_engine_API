from typing import List, Dict, Optional
from sqlalchemy import ForeignKey, String, Boolean, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from datetime import datetime
from app.billing_lead_types import (
    LeadSources,
    LeadActions,
    LeadQuality,
    BillableStatus,
)


# this is where we define our tables
class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__: str = "customers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )


class Product(Base):
    __tablename__: str = "products"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )


class Lead(Base):
    __tablename__: str = "leads"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), index=True)
    lead_type: Mapped[LeadSources] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )  # comes populated in POST req payload, no default

    customer: Mapped["Customer"] = relationship("Customer", back_populates="leads")
    product: Mapped["Product"] = relationship("Product", back_populates="leads")
    actions: Mapped[List["Action"]] = relationship("Action", back_populates="leads")


class Action(Base):
    __tablename__: str = "actions"
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


class BillingReport(Base):
    __tablename__: str = "billing_reports"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    billing_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), index=True
    )
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    reported_actions: Mapped[List[Action]] = relationship(
        "Action", back_populates="billingreport"
    )
    # list of dicts with product_id mapped to its subtotal cost
    totals_by_product: Mapped[Optional[List[Dict[str, Numeric]]]] = mapped_column(
        JSON
    )  # serialized for storage purposes
    total_amount: Mapped[Numeric] = mapped_column(Numeric, nullable=False)
    savings_amount: Mapped[Optional[Numeric]] = mapped_column(Numeric, default=0.0)
