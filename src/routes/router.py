
from flask import Blueprint, jsonify, request, send_from_directory
from src.models.TaxiModel import TaxiModel
from src.models.LocationModel import LocationModel
from src.models.entities.TaxiEntity import Taxi
from src.config import Config
from flask_swagger_ui import get_swaggerui_blueprint

main_bp = Blueprint("main_bp", __name__)
taxi_bp = Blueprint("taxi_bp", __name__)
location_bp = Blueprint("location_bp", __name__)

# Swagger configuration
SWAGGER_URL = Config.SWAGGER_URL
API_URL = Config.API_URL


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Fleet Management API"
    }
)

# Routes


@main_bp.route('/apidocs/swagger.json')
def swagger_json():
    return send_from_directory('static', 'swagger.json')


@main_bp.route('/')
def index():
    return jsonify({'message': 'Main Page'})


@taxi_bp.route('/taxi', methods=['GET'])
def get_taxies_list():
    try:
        # request.args.get('page', 1): Esto obtiene el valor del parámetro "page" de la URL de la solicitud HTTP. Se utiliza el valor predeterminado de 1, si no dice.
        page = int(request.args.get('page', 1))
        # Por defecto, 10 registros por página
        per_page = int(request.args.get('per_page', 10))

        taxies_paginated = TaxiModel.get_taxi(page=page, per_page=per_page)
        taxies_list = [taxi.to_JSON() for taxi in taxies_paginated.items]
        return jsonify({
            'taxies': taxies_list,
            'total_pages': taxies_paginated.pages,
            'current_page': taxies_paginated.page
        }), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@location_bp.route('/location', methods=['GET'])
def get_locations_list():
    try:
        date_requested = (request.args.get('date'))
        taxi_id = (request.args.get('taxi_id'))
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        locations_paginated = LocationModel.get_location_by_date_and_taxi(
            taxi_id=taxi_id, date_requested=date_requested, page=page, per_page=per_page)
        locations_list = [location.to_JSON()
                          for location in locations_paginated.items]
        return jsonify({
            'locations': locations_list,
            'total_pages': locations_paginated.pages,
            'current_page': locations_paginated.page
        }), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
