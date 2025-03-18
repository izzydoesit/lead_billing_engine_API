from typing import List, Dict, Optional
from sqlalchemy import ForeignKey, String, Boolean, Integer, Float, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


# this is where we define our tables
class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__: str = "leads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False, index=True
    )
    lead_type: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)


class Action(Base):
    __tablename__: str = "actions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    lead_type: Mapped[str] = mapped_column(String(30), nullable=False)
    action_type: Mapped[str] = mapped_column(String(30), nullable=False)
    engagement_level: Mapped[str] = mapped_column(String(10), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    billing_report_id: Mapped[int] = mapped_column(
        ForeignKey("billing_reports.id"), index=True
    )
    cost_amount: Mapped[Optional[float]] = mapped_column(Float, default=None)
    is_duplicate: Mapped[Optional[bool]] = mapped_column(Boolean, default=None)
    status: Mapped[Optional[str]] = mapped_column(String(20), default=None)


class Customer(Base):
    __tablename__: str = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class Product(Base):
    __tablename__: str = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class BillingReport(Base):
    __tablename__: str = "billing_reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    billing_date: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), index=True
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True
    )
    customer_name: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_email: Mapped[str] = mapped_column(String(50), nullable=False)
    actions: Mapped[List["Action"]] = relationship()
    # list of dicts with product_id, product_name and total_amount
    totals_by_product: Mapped[Optional[List[Dict[int, any]]]] = mapped_column(JSON)
    total_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=False)
    savings_amount: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
