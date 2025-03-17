from sqalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqalchemy.orm import relationship
from .database import Base

# this is where we define our tables

class Lead(Base):
    __tablename__ = "leads"
    lead_id = Column(Integer, primary_key=True, index=True)
    lead_type = Column(String, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    cost = Column(Float, nullable=True)

class Action(Base):
    __tablename__ = "actions"
    action_id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String, index=True)
    engagement_level = Column(String)
    lead_id = Column(Integer, ForeignKey("leads.lead_id"), index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), index=True)
    cost_amount = Column(Float)

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

class BillingReport(Base):
    __tablename__ = "billing_reports"
    billing_report_id = Column(Integer, primary_key=True, index=True)
    billing_date = Column(DateTime, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), index=True)
    customer_name = Column(String, index=True)
    customer_email = Column(String, index=True)
    total_amount = Column(Float)
    savings_amount = Column(Float, nullable=True)