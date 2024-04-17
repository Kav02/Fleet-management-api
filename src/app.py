from flask import Flask
from src.config import config
from src.database.db import connect_to_db
from src.routes.router import SWAGGER_URL, main_bp, taxi_bp, swaggerui_blueprint, location_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Conect to database
    connect_to_db(app)
    # Register blueprints

    app.register_blueprint(main_bp)
    app.register_blueprint(taxi_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app


# app = create_app('development')

# if __name__ == '__main__':
#     # app.config.from_object(config['development'])

#     app.run()
