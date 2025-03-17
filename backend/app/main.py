from fastapi import FastAPI
import models
from .database import engine

from .api.endpoints import health
from .api.endpoints import leads
from .api.endpoints import billing_reports

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(health.router, tags=["health"])
app.include_router(leads.router, tags=["leads"])
app.include_router(billing_reports.router, tags=["billing_reports"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
