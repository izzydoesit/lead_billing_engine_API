import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from datetime import datetime
from uuid import uuid4

from app.main import app
from app.core.database import get_async_session, Base
from app.models import Lead, Customer, Product, Action
from app.schemas import LeadCreate, CustomerCreate, ProductCreate, ActionCreate

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test_db"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture
def test_client(test_session):
    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_async_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def test_customer(test_session):
    customer = Customer(id=str(uuid4()), name="Test Customer", email="test@example.com")
    test_session.add(customer)
    await test_session.commit()
    return customer


@pytest.fixture
async def test_product(test_session):
    product = Product(
        id=str(uuid4()), name="Test Product", description="Test Description"
    )
    test_session.add(product)
    await test_session.commit()
    return product
