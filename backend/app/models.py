from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy import ForeignKey, String, Boolean, Float
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


# this is where we define our tables
class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__: str = "leads"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_type: Mapped[str] = mapped_column(String(30))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))


class Action(Base):
    __tablename__: str = "actions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    action_type: Mapped[str] = mapped_column(String(30))
    lead_type: Mapped[str] = mapped_column(String(30))
    engagement_level: Mapped[str] = mapped_column(String(10), nullable=False)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    billing_report_id: Mapped[int] = mapped_column(
        ForeignKey("billing_reports.id"), index=True
    )
    cost_amount: Mapped[Optional[float]] = mapped_column(nullable=True)
    is_duplicate: Mapped[Optional[bool]] = mapped_column(Boolean)
    status: Mapped[Optional[str]] = mapped_column(String(20), default=None)


class Customer(Base):
    __tablename__: str = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), index=True)


class Product(Base):
    __tablename__: str = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), index=True)
    description: Mapped[str] = mapped_column(String(50))


class BillingReport(Base):
    __tablename__: str = "billing_reports"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    billing_date: Mapped[datetime] = mapped_column(index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    customer_name: Mapped[str] = mapped_column(String(50))
    customer_email: Mapped[str] = mapped_column(String(50))
    actions: Mapped[List["Action"]] = relationship()
    # list of dicts with product_id, product_name and total_amount
    totals_by_product: Mapped[Optional[Dict[int, any]]] = mapped_column(JSON)
    total_amount: Mapped[Optional[float]] = mapped_column(default=0.0)
    savings_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
