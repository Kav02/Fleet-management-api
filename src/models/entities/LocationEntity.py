from sqlalchemy import Integer, Float, ForeignKey, DateTime
from src.database.db import db


class Location(db.Model):
    '''
    Represents a location entity in the fleet management system.

    Attributes:
        id (int): The unique identifier for the location.
        taxi_id (int): The ID of the taxi associated with the location.
        date (datetime): The date and time of the location.
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.
    '''

    __tablename__ = 'trajectories'

    id = db.Column(Integer, primary_key=True)
    taxi_id = db.Column(Integer, ForeignKey('taxis.id'), nullable=False)
    date = db.Column(DateTime(timezone=False), nullable=True)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)

    def to_dict(self):
        '''
        Converts the Location object to a dictionary.
        Returns:
            dict: A dictionary representation of the Location object.
        '''
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
