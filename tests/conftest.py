from datetime import datetime
import pytest
from src.app import create_app
from unittest.mock import patch
from src.database import db


@pytest.fixture
def app():
    app = create_app('development')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app_context():
    app = create_app()
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
        {
            'id': 1,
            'plate': 'ABC123',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'date': datetime(2022, 1, 1, 12, 0, 0)
        },
        {
            'id': 2,
            'plate': 'DEF456',
            'latitude': 34.0522,
            'longitude': -118.2437,
            'date': datetime(2022, 1, 2, 10, 30, 0)
        }
    ]
