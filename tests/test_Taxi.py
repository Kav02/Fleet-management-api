from src.app import create_app
from flask_testing import TestCase
from src.routes import router
import pytest
from src.models.entities.TaxiEntity import Taxi


def test_taxi_repr():
    # Given: Taxi values
    taxi_id = 1
    taxi_plate = 'ABC123'
    expected_repr = f"<Taxi(id={taxi_id}, plate='{taxi_plate}')>"

    # When: An instance of Taxi is created
    taxi = Taxi(id=taxi_id, plate=taxi_plate)

    # Then: The repr of the taxi is as expected
    assert repr(taxi) == expected_repr


def test_taxi_to_json():
    # Given: A Taxi object is instantiated with an id and a plate
    taxi_id = 241
    taxi_plate = 'GRF558'
    taxi = Taxi(id=taxi_id, plate=taxi_plate)
    # When: The to_JSON method is called on the Taxi object
    json_data = taxi.to_JSON()
    # Then: The Taxi object is converted to a JSON representation
    assert json_data == {'id': taxi_id, 'plate': taxi_plate}
