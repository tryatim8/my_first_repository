import pytest
from fastapi.testclient import TestClient

from homework.app.database import async_session
from homework.app.main import connect_routes, create_app, lifespan


@pytest.fixture
def app():
    _app = create_app(_lifespan=lifespan)
    connect_routes(app=_app, async_session=async_session)
    yield _app


@pytest.fixture
def client(app):
    client = TestClient(app)
    yield client
