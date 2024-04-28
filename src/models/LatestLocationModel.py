from datetime import datetime
import json
from .entities.LocationEntity import Location
from .entities.TaxiEntity import Taxi
from sqlalchemy import func, select
from flask import jsonify
from src.database.db import db


class LatestLocationModel():
    @classmethod
    def get_latest_location(cls):
        try:
            subquery = Location.query.with_entities(
                Location.taxi_id, func.max(Location.date).label('latest_date')).group_by(Location.taxi_id).subquery()

            latest_locations = db.session.query(
                Taxi.id,
                Taxi.plate,
                Location.latitude,
                Location.longitude,
                Location.date
            ).join(
                Location, Taxi.id == Location.taxi_id
            ).join(
                subquery,
                (Location.taxi_id == subquery.c.taxi_id) & (
                    Location.date == subquery.c.latest_date)
            )

            results = latest_locations.all()

            return results

        except Exception as ex:
            raise Exception(ex)

    @ classmethod
    def latest_to_json(cls, results):
        latest_location_json = []
        for result in results:
            location_data = {
                'id': result.id,
                'plate': result.plate,
                'latitude': result.latitude,
                'longitude': result.longitude,
                # Convertir la fecha
                'date': result.date.isoformat()

            }
            latest_location_json.append(location_data)
            print(latest_location_json)
        return latest_location_json
