# from src.app import create_app
# from src.routes import router
import pytest
from src.models.entities.LocationEntity import Location


def test_location_repr():
    # Given: Location values
    location_id = 125
    location_taxi_id = 6418
    location_date = 'Sat, 02 Feb 2008 15:48:08 GMT'
    location_latitude = 116.32745
    location_longitude = 39.93256
    expected_repr = f"<Trajectorie(id={location_id}, taxi_id ='{location_taxi_id}', date = '{location_date}',latitude = '{location_latitude}',longitude = '{location_longitude}')>"

    # When: An instance of Location is created
    location = Location(id=location_id,
                        taxi_id=location_taxi_id,
                        date=location_date,
                        latitude=location_latitude,
                        longitude=location_longitude
                        )

    # Then: The repr of the taxi is as expected
    assert repr(location) == expected_repr


def test_location_to_json():
    # Given: A Taxi object is instantiated with an id and a plate
    location_id = 125
    location_taxi_id = 6418
    location_date = 'Sat, 02 Feb 2008 15:48:08 GMT'
    location_latitude = 116.32745
    location_longitude = 39.93256
    location = Location(id=location_id,
                        taxi_id=location_taxi_id,
                        date=location_date,
                        latitude=location_latitude,
                        longitude=location_longitude)
    # When: The to_JSON method is called on the Taxi object
    json_data = location.to_JSON()
    # Then: The Taxi object is converted to a JSON representation
    assert json_data == {'id': location_id, 'taxi_id': location_taxi_id,
                         'date': location_date, 'latitude': location_latitude, 'longitude': location_longitude}
