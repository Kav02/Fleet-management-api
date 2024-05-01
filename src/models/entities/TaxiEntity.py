from sqlalchemy import Integer, String
from src.database.db import db


class Taxi(db.Model):
    """_summary_

    Returns:
        _type_: _description_
    """

    __tablename__ = 'taxis'

    id = db.Column(Integer, primary_key=True)
    plate = db.Column(String(20), nullable=False)

    def to_dict(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
