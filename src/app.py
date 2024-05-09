from flask import Flask
from src.config import config
from src.database.db import connect_to_db
from src.routes.router import SWAGGER_URL, main_bp, taxi_bp, swaggerui_bp, location_bp


def create_app(config_name):
    '''
    Create and configure the Flask application.
    Parameters:
    - config_name (str): The name of the configuration to use for the application.
    Returns:
    - app (Flask): The configured Flask application.
    '''

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Connect to database
    connect_to_db(app)
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(taxi_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    return app
