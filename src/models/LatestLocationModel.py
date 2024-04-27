from .entities.LocationEntity import Location
from .entities.TaxiEntity import Taxi
from sqlalchemy import func, select
from flask import jsonify


class LatestLocationModel():
    @classmethod
    def get_latest_location(cls):
        try:
            latest_locations = (Location.query(
                Location.taxi_id, func.max(Location.date).group).all())
            print(len(latest_locations))
            return latest_locations
        except Exception as ex:
            raise Exception(ex)

    @ classmethod
    def latest_to_json(cls, results):
        latest_location_json = []
        for result in results:
            location_data = {
                'id': result[0],
                'plate': result[1],
                'latitude': result[2],
                'longitude': result[3],
                # Convertir la fecha a formato ISO para JSON
                'date': result[4].isoformat()
            }
            latest_location_json.append(location_data)
        return latest_location_json
