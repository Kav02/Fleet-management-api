from flask_sqlalchemy import SQLAlchemy, session
from src.config import Config

db = SQLAlchemy()


def connect_to_db(app):
    '''
    Connects the application to the database.
    Args:
        app: The Flask application object.
    Returns:
        None
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
