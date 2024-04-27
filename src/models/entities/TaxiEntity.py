from sqlalchemy import Column, Integer, String
from src.database.db import db


class Taxi(db.Model):
    __tablename__ = 'taxis'

    id = db.Column(Integer, primary_key=True)
    plate = db.Column(String(20), nullable=False)

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    # def to_JSON(self):
    #     return {
    #         'id': self.id,
    #         'plate': self.plate
    #     }
# Magic method __repr__: returns a readable representation of an object
