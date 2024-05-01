from .conftest import app
from src.models.entities.LocationEntity import Location
from src.models.LocationModel import LocationModel
from datetime import datetime


def test_to_dict():
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
    # When: The toDict is called on the Taxi object
    location_dict = location.to_dict()
    # Then: The Taxi object is converted to a dictionary
    assert location_dict['id'] == location_id
    assert location_dict['taxi_id'] == location_taxi_id
    assert location_dict['date'] == location_date
    assert location_dict['latitude'] == location_latitude
    assert location_dict['longitude'] == location_longitude


def test_get_location_by_date_and_taxi(app, client):
    # Given: I want to get the location by date and taxi
    taxi_id = 6418
    date_requested = datetime(2008, 2, 2, 15, 48, 8)
    page = 1
    per_page = 10

    with app.app_context():

        # When: The get_location_by_date_and_taxi method is called
        location_paginated = LocationModel.get_location_by_date_and_taxi(
            taxi_id=taxi_id, date_requested=date_requested, page=page, per_page=per_page)

    # Then: The list of Taxi objects is returned: Length of the list, and the number of pages
    assert len(location_paginated.items) == per_page
    assert location_paginated.page == page
    assert location_paginated.pages == 14
