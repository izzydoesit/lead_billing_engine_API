from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from .base import Base
from .customer import Customer
from .product import Product
from backend.app.shared.billing_lead_types import LeadSources


class Lead(Base):
    __tablename__ = "leads"
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
