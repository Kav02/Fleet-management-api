from src.models.entities.TaxiEntity import Taxi
from src.models.TaxiModel import TaxiModel
from .conftest import app


def test_to_dict():
    """
    Test case for the to_dict method of the Taxi class.

    This test verifies that the Taxi object is correctly converted to a dictionary
    when the to_dict method is called.
    """
    # Given: A Taxi object is instantiated with an id and a plate
    taxi_id = 241
    taxi_plate = 'GRF558'
    taxi = Taxi(id=taxi_id, plate=taxi_plate)
    # When: The to_dict is called on the Taxi object
    taxi_dict = taxi.to_dict()
    # Then: The Taxi object is converted to dictionary
    assert taxi_dict['id'] == taxi_id
    assert taxi_dict['plate'] == taxi_plate


def test_get_taxi(app, client):
    """
    Test case for the get_taxi method.

    Args:
        app: The Flask application object.
        client: The Flask test client.

    Returns:
        None

    Raises:
        AssertionError: If the test fails.

    """
    # Given: A list of Taxi objects
    page = 1
    per_page = 20

    with app.app_context():

        # When: The get_taxi method is called
        taxis_paginated = TaxiModel.get_taxi(page=page, per_page=per_page)
    # Then: The list of Taxi objects is returned: Length of the list, the first item, and the number of pages
    assert len(taxis_paginated.items) == per_page
    assert taxis_paginated.pages == 10
    assert taxis_paginated.page == 1
