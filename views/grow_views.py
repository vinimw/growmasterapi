from quart import Blueprint, request, jsonify
from utils import fetch_external_data, post_external_data, build_request_params, build_request_params_post, build_request_params_patch, patch_external_data, build_request_params_delete, delete_external_data
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

@grow_bp.route('/api/grows/update', methods=['POST'])
@token_required
async def edit_plant():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split('Bearer ')[1]

    data = await request.get_json()
    
    # Lista de campos obrigatórios
    required_fields = ['id_update']

    # Verificação de campos ausentes
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'fields': missing_fields}), 400

    id_update = data.get('id_update')

    if id_update == '':
        return jsonify({'error': 'Missing required fields', 'field id_update must be different': 'empty'}), 400

    dataSend = {}
    if data.get('name') and data.get('name') != '':
        dataSend['name'] = data.get('name')
    if data.get('description') and data.get('description') != '':
        dataSend['description'] = data.get('description')

    url, headers = build_request_params_patch('grows', id_update)
    external_data, status = await patch_external_data(url, dataSend, headers)
    
    if status != 200:
        return jsonify(external_data), status

    return jsonify(external_data)

@grow_bp.route('/api/grows/delete', methods=['POST'])
@token_required
async def delete_plant():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split('Bearer ')[1]

    data = await request.get_json()
    
    # Lista de campos obrigatórios
    required_fields = ['id']

    # Verificação de campos ausentes
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'fields': missing_fields}), 400

    id = data.get('id')

    if id == '':
        return jsonify({'error': 'Missing required fields', 'field id must be different': 'empty'}), 400

    url, headers = build_request_params_delete('grows', id)
    external_data, status = await delete_external_data(url, headers)
    
    if status != 200:
        return jsonify(external_data), status

    return jsonify(external_data)
