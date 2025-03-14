from fastapi import FastAPI
from .api.endpoints import health
from .api.endpoints import leads
from .api.endpoints import billing_reports

app = FastAPI()

app.include_router(health.router, tags=["health"])
app.include_router(leads.router, tags=["leads"])
app.include_router(billing_reports.router, tags=["billing_reports"])
