import datetime
from unittest.mock import patch
from src.models.LatestLocationModel import LatestLocationModel


def test_get_latest_location(app):
    # Given: A locations in the database
    with app.app_context():
        # When: The latest locations are retrieved
        latest_locations = LatestLocationModel.get_latest_location()


        # Then: The result contains the expected values
        assert len(latest_locations) > 0

        for location in latest_locations:
            assert hasattr(location, 'id')
            assert hasattr(location, 'plate')
            assert hasattr(location, 'latitude')
            assert hasattr(location, 'longitude')
            assert hasattr(location, 'date')


@patch('src.models.LatestLocationModel.LatestLocationModel.get_latest_location')
def test_latest_to_json(mock_get_latest_location):
    class LocationObject:
        def __init__(self, id, plate, latitude, longitude, date):
            self.id = id
            self.plate = plate
            self.latitude = latitude
            self.longitude = longitude
            self.date = date
    mock_get_latest_location.return_value = [
        LocationObject(1, 'ABC123', 37.7749, -122.4194, datetime.datetime(2022, 1, 1, 12, 0, 0)),
        LocationObject(2, 'DEF456', 34.0522, -118.2437, datetime.datetime(2022, 1, 2, 10, 30, 0))
        ]
    json_data = LatestLocationModel.latest_to_json(mock_get_latest_location.return_value)
    print ('Json_data', json_data)
    # Assert the expected JSON data
    expected_json = [
        {
            'id': 1,
            'plate': 'ABC123',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'date': '2022-01-01T12:00:00'
        },
        {
            'id': 2,
            'plate': 'DEF456',
            'latitude': 34.0522,
            'longitude': -118.2437,
            'date': '2022-01-02T10:30:00'
        }
    ]
    assert json_data == expected_json
