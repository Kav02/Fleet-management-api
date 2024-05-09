from sqlalchemy import func
from .entities.LocationEntity import Location


class LocationModel():
    ''' Represents a model for retrieving location data for taxis.'''

    @classmethod
    def get_location_by_date_and_taxi(cls, taxi_id, date_requested, page=1, per_page=10):
        ''' Retrieves location data for a specific taxi on a specific date.'''
        try:
            location_list = Location.query.filter(
                func.date(Location.date) == date_requested, Location.taxi_id == taxi_id)
            #func.date(Location.date) convierte el objeto de fecha y hora, en una fecha (eliminando la parte de la hora).
            location_paginated = location_list.paginate(
                page=page, per_page=per_page)
            return location_paginated
        except Exception as ex:
            raise Exception(ex)
