"""
This module contains the routes for the Fleet Management API.
"""
from datetime import datetime
from flask import Blueprint, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from src.config import Config
from src.models.LatestLocationModel import LatestLocationModel
from src.models.LocationModel import LocationModel
from src.models.TaxiModel import TaxiModel

main_bp = Blueprint("main_bp", __name__)
taxi_bp = Blueprint("taxi_bp", __name__)
location_bp = Blueprint("location_bp", __name__)

# Swagger configuration
SWAGGER_URL = Config.SWAGGER_URL
API_URL = Config.API_URL


swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Fleet Management API"
    }
)

# Routes


@main_bp.route('/apidocs/swagger.json')
def swagger_json():
    '''Returns the swagger.json file.'''
    return send_from_directory('static', 'swagger.json')


@main_bp.route('/')
def index():
    '''Main Page'''
    return jsonify({'message': 'Main Page'})


@taxi_bp.route('/taxi', methods=['GET'])
def get_taxis_list():
    '''Returns a list of taxis paginated.'''
    try:
        # request... Gets the value of the “page” parameter of the HTTP URL.
        page = int(request.args.get('page', 1))
        # Default, 10 records per page
        per_page = int(request.args.get('per_page', 10))
        taxis_paginated = TaxiModel.get_taxi(page=page, per_page=per_page)
        # taxis_list = [taxi.to_JSON() for taxi in taxis_paginated.items]
        taxis_list = []
        for taxi in taxis_paginated.items:
            taxis_list.append(taxi.to_dict())

        return jsonify({
            'taxis': taxis_list,
            'total_pages': taxis_paginated.pages,
            'current_page': taxis_paginated.page
        }), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@ location_bp.route('/location', methods=['GET'])
def get_locations_list():
    '''Returns the locations paginated. '''
    date_requested = request.args.get('date')
    taxi_id = request.args.get('taxi_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    if not (date_requested and taxi_id):
        return jsonify({'error': 'Both date and taxi_id are required.'}), 400
    try:
        specific_date = datetime.strptime(date_requested, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'})

    try:
        locations_paginated = LocationModel.get_location_by_date_and_taxi(
            taxi_id=taxi_id, date_requested=specific_date, page=page, per_page=per_page)
        # locations_list = [location.to_JSON()
        #                 for location in locations_paginated.items]  # Dictionaries are not iterable directly using for. The .items method provides a way to iterate over both the keys and values.
        locations_list = []
        for location in locations_paginated.items:
            locations_list.append(location.to_dict())
        return jsonify({
            'locations': locations_list,
            'total_pages': locations_paginated.pages,
            'current_page': locations_paginated.page
        }), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@ location_bp.route('/location/latest', methods=['GET'])
def get_latest_location_list():
    '''Returns the latest locations paginated.'''
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        latest_location = LatestLocationModel.get_latest_location(
        )
        # print(latest_location)
        total_pages = len(latest_location) // per_page
        if len(latest_location) % per_page != 0:
            total_pages += 1

        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        paginated_locations = latest_location[start_index:end_index]
        latest_list = LatestLocationModel.latest_to_json(
            paginated_locations)
        # print(latest_list)
        return jsonify({
            'locations': latest_list,
            'total_pages': total_pages,
            'current_page': page
        }), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
