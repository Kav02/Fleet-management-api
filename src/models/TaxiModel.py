from src.models.entities.TaxiEntity import Taxi


class TaxiModel():
    '''TaxiModel class to get data from Taxi entity'''
    @classmethod
    def get_taxi(cls, page=1, per_page=20):

        try:
            taxis_paginated = Taxi.query.paginate(
                page=page, per_page=per_page)
            return taxis_paginated
        except Exception as ex:
            raise Exception(ex)
