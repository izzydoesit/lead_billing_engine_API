from fastapi import FastAPI
from .api.endpoints import health

app = FastAPI()

app.include_router(health.router, tags=["health"])
