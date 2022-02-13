import pytest

from app.app import create_app
from app.database import Session
from app.services.genres import GenresService
from app.services.shows import ShowsService


@pytest.fixture(scope="function")
def test_client():
    app = create_app()
    client = app.test_client()

    return client


@pytest.fixture(scope="function")
def session():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture(scope="function")
def shows_service(session):
    return ShowsService(session)


@pytest.fixture(scope="function")
def genres_service(session):
    return GenresService(session)
