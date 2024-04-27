from .entities.TaxiEntity import Taxi


class TaxiModel():

    @classmethod
    def get_taxi(cls, page=1, per_page=20):

        try:
            taxies_paginated = Taxi.query.paginate(
                page=page, per_page=per_page)
            return taxies_paginated
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_taxi_as_json(cls):
        try:
            taxies = cls.get_taxi()
            taxies_json = [taxi.to_JSON() for taxi in taxies]
            return taxies_json
        except Exception as ex:
            raise Exception(ex)
