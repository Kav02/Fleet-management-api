

import pytest
from src.config import Config, config


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Main Page' in response.data
