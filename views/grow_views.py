from quart import Blueprint, request, jsonify
from utils import fetch_external_data, post_external_data, build_request_params, build_request_params_post
from auth import token_required

grow_bp = Blueprint('grow_bp', __name__)

@grow_bp.route('/api/grows', methods=['GET'])
@token_required
async def get_plants():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split('Bearer ')[1]

    query_params = {'user': token}
    url, headers = build_request_params('grows', query_params)
    external_data, status = await fetch_external_data(url, headers)
    
    if status != 200:
        return jsonify(external_data), status

    return jsonify(external_data)

@grow_bp.route('/api/grows', methods=['POST'])
@token_required
async def add_plant():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split('Bearer ')[1]

    data = await request.get_json()
    
    # Lista de campos obrigatórios
    required_fields = ['name']

    # Verificação de campos ausentes
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'fields': missing_fields}), 400

    dataSend = {
        "user": token,
        "name": data.get('name'),
        "description": data.get('description', ''),
    }

    url, headers = build_request_params_post('grows')
    external_data, status = await post_external_data(url, dataSend, headers)
    
    if status != 200:
        return jsonify(external_data), status

    return jsonify(external_data)



