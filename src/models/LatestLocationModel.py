from sqlalchemy import func
from src.database.db import db
from src.models.entities.LocationEntity import Location
from src.models.entities.TaxiEntity import Taxi


class LatestLocationModel():
    """
    Represents a model for retrieving the latest location data for taxis.
    """

    @classmethod
    def get_latest_location(cls):
        """
        Retrieves the latest location data for taxis.

        Returns:
            A list of tuples containing the latest location data for each taxi.
        """
        try:
            # with entities to load specific columns
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

    @classmethod
    def latest_to_json(cls, results):
        """
        Converts the latest location data to JSON format.

        Args:
            results: A list of tuples containing the latest location data for each taxi.

        Returns:
            A list of dictionaries representing the latest location data in JSON format.
        """
        latest_location_json = []
        for result in results:
            location_data = {
                'id': result.id,
                'plate': result.plate,
                'latitude': result.latitude,
                'longitude': result.longitude,
                # Convert the date
                'date': result.date.isoformat()

            }
            latest_location_json.append(location_data)
        return latest_location_json
