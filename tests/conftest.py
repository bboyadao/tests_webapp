import asyncio
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import app

sys.path.append(str(Path(__file__).resolve().parents[1]))


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="function")
def override_dependencies():
    """
    from app.dependencies import get_db
    async def fake_db():
        yield FakeSession()
    app.dependency_overrides[get_db] = fake_db

    Sau test, xoá override.
    """
    # app.dependency_overrides[get_db] = fake_db
    yield
    app.dependency_overrides = {}
