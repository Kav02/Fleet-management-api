import requests


## Test for get_taxis_list
def test_get_taxis_status_code(base_url):
    """Tests that the GET request to '/taxis' endpoint returns a 200 status code."""
    url = f"{base_url}/taxi"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def test_get_taxis_body(base_url):
    """Tests that the response body from the GET request to '/taxis' endpoint contains a 'taxis' property."""
    url = f"{base_url}/taxi"
    response = requests.get(url, timeout=5)
    data = response.json()
    assert "taxis" in data
    assert 'total_pages' in data
    assert 'current_page' in data

def test_get_taxis_list_invalid_page(client):
    """Tests error handling for invalid page number (non-integer)."""
    response = client.get('/taxi', query_string={'page': 'abc', 'per_page': 10})
    assert response.status_code == 500

    data = response.json
    assert 'message' in data
    assert 'invalid literal for int() with base 10:' in data['message']  # Specific error message

def test_get_taxis_list_invalid_per_page(client):
    """Tests error handling for invalid per_page value (non-integer)."""
    response = client.get('/taxi', query_string={'page': 1, 'per_page': 'xyz'})
    assert response.status_code == 500


## Test for get_locations_list
def test_get_location_status_code(client):
    """Tests that the GET request to '/location' endpoint returns a 200 status code."""
    response = client.get('/location', query_string={'taxi_id': '6418', 'date': '2008-02-02'})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"


def test_get_location_list_invalid_taxi(client):
    """Tests error handling for invalid taxi id."""
    response = client.get('/location', query_string={'taxi_id': 'abc', 'date': '2008-02-02'})
    assert response.status_code == 500


def test_get_location_list_missing_date(client):
    """Tests error handling for missing date value."""
    response = client.get('/location', query_string={'taxi_id': 6418})
    assert response.status_code == 400

## Test for get_latest_locations_list
def test_get_latest_location_status_code(base_url):
    """Tests that the GET request to '/location/latest' endpoint returns a 200 status code."""
    url = f"{base_url}/location/latest"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def test_get_latest_location_body(base_url):
    """Tests that the response body from the GET request to '/location/latest' endpoint contains a 'taxis' property."""
    url = f"{base_url}/location/latest"
    response = requests.get(url, timeout=5)
    data = response.json()
    assert "locations" in data
    assert 'total_pages' in data
    assert 'current_page' in data

def test_get_latest_location_invalid_params(client):
    """Tests error handling for invalid 'page' and 'per_page' parameters."""
    invalid_params = [
        {'page': 'abc', 'per_page': 10},
        {'page': 1, 'per_page': 'xyz'},
    ]
    for params in invalid_params:
        response = client.get('/location/latest', query_string=params)
        expected_status = 500
        assert response.status_code == expected_status, f"Expected status {expected_status} for invalid params: {params}"
