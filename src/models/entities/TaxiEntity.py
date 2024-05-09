from sqlalchemy import Integer, String
from src.database.db import db


class Taxi(db.Model):
    ''' Represents a taxi entity in the fleet management system.'''

    __tablename__ = 'taxis'

    id = db.Column(Integer, primary_key=True)
    plate = db.Column(String(20), nullable=False)

    def to_dict(self):
        ''' Converts the Taxi object to a dictionary.'''
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
