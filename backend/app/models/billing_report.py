from sqlalchemy import String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.dialects.postgresql import JSON
from .models import ModelBase
from .action import Action


class BillingReport(ModelBase):
    __tablename__ = "billing_reports"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    # totals_by_product: Mapped[Optional[List[Dict[str, Numeric]]]] = mapped_column(
    #     JSON
    # )  # serialized for storage purposes
    total_billed_amount: Mapped[Numeric] = mapped_column(Numeric, nullable=False)
    savings_amount: Mapped[Optional[Numeric]] = mapped_column(Numeric, default=0.0)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), index=True
    )
    actions: Mapped[List["Action"]] = relationship(
        "Action", back_populates="billing_report"
    )
    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="billing_reports"
    )
    # billing_report_file: Mapped["BillingReportFile"] = relationship(
    #     "BillingReportFile", back_populates="billing_report"
    # )
