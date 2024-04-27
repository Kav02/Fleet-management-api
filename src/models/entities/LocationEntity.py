from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from src.database.db import db
from sqlalchemy.dialects.postgresql import JSON


class Location(db.Model):
    __tablename__ = 'trajectories'

    id = db.Column(Integer, primary_key=True)
    taxi_id = db.Column(Integer, ForeignKey('taxis.id'), nullable=False)
    date = db.Column(DateTime(timezone=False), nullable=True)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}

    # def __repr__(self):
    #     return f"<Trajectorie(id={self.id}, taxi_id ='{self.taxi_id}', date = '{self.date}',latitude = '{self.latitude}',longitude = '{self.longitude}')>"

    # def to_JSON(self):
    #     return {
    #         'id':  self.id,
    #         'taxi_id': self.taxi_id,
    #         'date': self.date,
    #         'latitude': self.latitude,
    #         'longitude': self.longitude
    #     }
