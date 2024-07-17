from quart import Blueprint, request, jsonify
from utils import fetch_external_data, post_external_data, build_request_params, build_request_params_post
from auth import token_required

plant_bp = Blueprint('plant_bp', __name__)

@plant_bp.route('/api/plants', methods=['GET'])
@token_required
async def get_plants():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split('Bearer ')[1]

    query_params = {'user': token}
    url, headers = build_request_params('plants', query_params)
    external_data, status = await fetch_external_data(url, headers)
    
    if status != 200:
        return jsonify(external_data), status

    return jsonify(external_data)

@plant_bp.route('/api/plants', methods=['POST'])
@token_required
async def add_plant():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split('Bearer ')[1]

    data = await request.get_json()
    
    # Lista de campos obrigatórios
    required_fields = ['name', 'status', 'grow', 'created']

    # Verificação de campos ausentes
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': 'Missing required fields', 'fields': missing_fields}), 400

    # Definindo os campos opcionais com valores padrão vazios se não estiverem presentes
    # optional_fields = ['last_water', 'description', 'flower_date', 'yield']

    statusPlant = data.get('status')

    if statusPlant != 'VEG' and statusPlant != 'BLOOM':
        return jsonify({'error': 'Missing required fields', 'field status mues be': 'VEG or BLOOM'}), 400

    dataSend = {
        "user": token,
        "name": data.get('name'),
        "status": data.get('status'),
        "grow": data.get('grow'),
        "created": data.get('created'),
        "last_water": data.get('last_water', ''),
        "description": data.get('description', ''),
        "flower_date": data.get('flower_date', ''),
        "yield": data.get('yield', '')
    }
    
    url, headers = build_request_params_post('plants')
    external_data, status = await post_external_data(url, dataSend, headers)
    
    if status != 200:
        return jsonify(external_data), status

    return jsonify(external_data)


