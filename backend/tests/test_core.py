import pytest
from app.core.database import get_async_session, check_database_status


async def test_database_connection(test_session):
    status = await check_database_status()
    assert status is True


async def test_get_session():
    session = await anext(get_async_session())
    assert session is not None
