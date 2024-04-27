from .entities.LocationEntity import Location
from sqlalchemy import func

from flask import jsonify


class LocationModel():

    @classmethod
    def get_location_by_date_and_taxi(cls, taxi_id, date_requested, page=1, per_page=10):

        try:
            location_list = Location.query.filter(
                func.date(Location.date) == date_requested.date(), Location.taxi_id == taxi_id)
            location_paginated = location_list.paginate(
                page=page, per_page=per_page)
            return location_paginated
        except Exception as ex:
            raise Exception(ex)

    # @classmethod
    # def get_location_as_json(cls):
    #     try:
    #         locations = cls.get_location()
    #         locations_json = [location.to_JSON()
    #                           for location in locations]
    #         return locations_json
    #     except Exception as ex:
    #         raise Exception(ex)
