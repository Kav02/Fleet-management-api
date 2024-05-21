from sqlalchemy import Integer, Float, ForeignKey, DateTime
from src.database.db import db


class Location(db.Model):
    '''Represents a location entity in the fleet management system.'''

    __tablename__ = 'trajectories'

    id = db.Column(Integer, primary_key=True)
    taxi_id = db.Column(Integer, ForeignKey('taxis.id'), nullable=False)
    date = db.Column(DateTime(timezone=False), nullable=True)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)

    def to_dict(self):
        #For each column, get the key and value and return it as a dictionary
        ''' Converts the Location object to a dictionary.'''
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
