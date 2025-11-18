import pytest

from app.main import app, health_check


@pytest.mark.asyncio
async def test_ping(async_client):
    url = app.router.url_path_for(health_check.__name__)
    c = await async_client.get(url)
    assert c.status_code == 200
    assert c.text == '"pong"'
