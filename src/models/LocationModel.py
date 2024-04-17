from .entities.LocationEntity import Location
from sqlalchemy import func
from datetime import datetime


class LocationModel():

    @classmethod
    def get_location_by_date_and_taxi(cls, taxi_id=None, date_requested=None, page=1, per_page=10):
        try:
            if taxi_id is not None and date_requested is not None:
                specific_date = datetime.strptime(date_requested, '%Y-%m-%d')
                location_list = Location.query.filter(
                    func.date(Location.date) == specific_date.date(), Location.taxi_id == taxi_id)
            else:
                location_list = Location.query

            location_paginated = location_list.paginate(
                page=page, per_page=per_page)
            return location_paginated
        except Exception as ex:
            raise Exception(ex)

        # Si el taxi es nulo y la fecha buscar la fecha y listar todos los taxis
        # Si la fecha es nula y # de taxi  mostrar todas la fechas para ese taxi
        # si se indica la fecha y el # de taxi mostrar ese detalle

    @classmethod
    def get_location_as_json(cls):
        try:
            locations = cls.get_location()
            locations_json = [location.to_JSON()
                              for location in locations]
            return locations_json
        except Exception as ex:
            raise Exception(ex)
