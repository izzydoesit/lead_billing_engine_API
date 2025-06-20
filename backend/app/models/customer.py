from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .models import ModelBase


class Customer(ModelBase):
    __tablename__: str = "customers"
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    leads: Mapped[list["Lead"]] = relationship(
        "Lead", back_populates="customer", lazy="joined"
    )
    actions: Mapped[list["Action"]] = relationship(
        "Action", back_populates="customer", lazy="joined"
    )
    billing_reports: Mapped[list["BillingReport"]] = relationship(
        "BillingReport", back_populates="customer", lazy="joined"
    )
