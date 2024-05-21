import sqlalchemy
from src.models.entities.TaxiEntity import Taxi


class TaxiModel():
    '''TaxiModel class to get data from Taxi entity'''
    @classmethod
    def get_taxi(cls, page=1, per_page=20):
        '''Get all taxis paginated'''
        try:
            taxis_paginated = Taxi.query.paginate(
                page=page, per_page=per_page)
            return taxis_paginated
        except Exception as ex:
            raise Exception(ex)
# Un @classmethod recibe la clase como primer argumento (cls),
# en lugar de una instancia de la clase (self).
# Esto permite que el método acceda y modifique atributos de clase y llame a otros métodos de clase.
# En lugar de crear una instancia de la clase, se llama directamente en la clase.