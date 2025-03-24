from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .models import ModelBase


class BillingReportFile(ModelBase):
    __tablename__ = "billing_report_files"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    billing_report_id: Mapped[str] = mapped_column(
        ForeignKey("billing_reports.id"), index=True
    )
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), index=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), index=True
    )
