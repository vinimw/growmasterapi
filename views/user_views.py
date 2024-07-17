from quart import Blueprint, request, jsonify
from utils import fetch_external_data, build_request_params
import config

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/user', methods=['POST'])
async def request_user():
    data = await request.get_json()
    login = data.get('login')
    password = data.get('password')

    if not login or not password or login == '' or password == '':
        return jsonify({'error': config.errorCodes[501]})

    query_params = {'email': login, 'password': password}
    url, headers = build_request_params('users', query_params)
    external_data, status = await fetch_external_data(url, headers)
    
    if status != 200:
        return jsonify(external_data), status
    
    if isinstance(external_data, list) and len(external_data) > 0:
        response = {
            "name": external_data[0]["name"],
            "email": external_data[0]["email"],
            "token": external_data[0]["id"]
        }
        return jsonify(response)
    return jsonify({'error': config.errorCodes[502]})
