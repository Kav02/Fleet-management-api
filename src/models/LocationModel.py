from .entities.LocationE import Location


class LocationModel():

    @classmethod
    def get_location(cls, page=1, per_page=10):
       # connection = connect_to_db()
        try:
            location_paginated = Location.query.paginate(
                page=page, per_page=per_page)
            return location_paginated
        except Exception as ex:
            raise Exception(ex)
        # finally:
        #     connection.close()

    @classmethod
    def get_location_as_json(cls):
        try:
            locations = cls.get_location()
            locations_json = [location.to_JSON()
                              for location in locations]
            return locations_json
        except Exception as ex:
            raise Exception(ex)
