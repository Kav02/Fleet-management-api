import datetime
from unittest.mock import patch
from .conftest import app
from src.models.LatestLocationModel import LatestLocationModel


# def test_latest_location_to_dict(app):
#     # Given: A locations in the database
#     with app.app_context():
#         # When: The latest locations are retrieved and converted to a dictionary
#         latest_locations = LatestLocationModel.get_latest_location()
#         latest_locations_dict = LatestLocationModel.latest_to_json(
#             latest_locations)

#         # Then: The converted dictionary contains the expected keys and values
#         assert len(latest_locations_dict) > 0
#         for location_dict in latest_locations_dict:
#             assert 'id' in location_dict
#             assert 'plate' in location_dict
#             assert 'latitude' in location_dict
#             assert 'longitude' in location_dict
#             assert 'date' in location_dict


# def test_get_latest_location_with_data(mocked_db_session):
#     # Given
#     # Mock data
#     mocked_results = [
#         (1,
#          'ABC-123',
#          10.23,
#          -54.78,
#          datetime.datetime(2024, 4, 29, 18, 32, 10)
#          ),
#         (2,
#          'DEF-456',
#          23.11,
#          -12.90,
#          datetime.datetime(2024, 4, 28, 14, 55, 22)
#          )
#     ]

#     # Set the mocked results for the query
#     mocked_db_session.query.return_value.join.return_value.all.return_value = mocked_results
#     print(mocked_db_session.query.return_value.join.return_value.all.return_value)
#     # Call the function under test
#     results = LatestLocationModel.get_latest_location()

#     # Assert the expected results

#     assert len(results) == len(mocked_results)
#     for i, result in enumerate(results):
#         assert result.id == mocked_results[i][0]
#         assert result.plate == mocked_results[i][1]
#         assert result.latitude == mocked_results[i][2]
#         assert result.longitude == mocked_results[i][3]
#         # Extract and compare actual date/time values (assuming you want to compare dates)
#         assert result.datetime.date() == mocked_results[i][4].date()


# Test cases for the LatestLocationModel


@patch('src.models.LatestLocationModel.db')
def test_get_latest_location(app_context, mock_session, results):

    # Mock the database session and query
    mock_session = mock_session.session.return_value
    mock_query = mock_session.query.return_value
    mock_query.join.return_value = mock_query
    mock_query.all.return_value = results

    # Call the method under test
    locations = LatestLocationModel.get_latest_location()

    # Assert the expected results
    assert locations == results


def test_latest_to_json(results):
    # Call the method under test
    json_data = LatestLocationModel.latest_to_json(results)

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
