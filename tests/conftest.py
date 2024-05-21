# test_conftest.py

from datetime import datetime
from unittest.mock import patch
import pytest
from src.app import create_app
from src.database import db

@pytest.fixture()
def base_url():
    """Provides the base URL of the API under test."""
    return "http://127.0.0.1:5000"

@pytest.fixture
def app():
    app = create_app('development')
    return app


@pytest.fixture
def client(app,client):
    return app.test_client()


@pytest.fixture
def app_context():
    app = create_app('development')
    with app.app_context():
        yield


@pytest.fixture
def mock_session(app):
    """Mocks the database session object for testing database interactions."""
    with patch.object(db, 'session') as mock_session:
        mock_session.query.return_value.join.return_value.all.return_value = results
        yield mock_session


@pytest.fixture

def results():
    return [
    (1, 'ABC123', 37.7749, -122.4194, datetime(2022, 1, 1, 12, 0, 0)),
    (2, 'DEF456', 34.0522, -118.2437, datetime(2022, 1, 2, 10, 30, 0))
    ]
