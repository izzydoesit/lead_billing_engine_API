from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from .models import ModelBase
from .customer import Customer
from .product import Product
from app.shared.lead_action_types import LeadTypes


class Lead(ModelBase):
    __tablename__ = "leads"
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, index=True, nullable=False
    )
    customer_id: Mapped[str] = mapped_column(
        String, ForeignKey("customers.id"), index=True, nullable=False
    )
    product_id: Mapped[str] = mapped_column(
        String, ForeignKey("products.id"), index=True, nullable=False
    )
    lead_type: Mapped[LeadTypes] = mapped_column(Enum(LeadTypes), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )  # comes populated in POST req payload, no default
    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="leads", lazy="joined"
    )
    product: Mapped["Product"] = relationship(
        "Product", back_populates="leads", lazy="joined"
    )
    actions: Mapped[List["Action"]] = relationship(
        "Action", back_populates="lead", lazy="joined"
    )
