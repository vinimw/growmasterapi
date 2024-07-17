from functools import wraps
from quart import request, jsonify
import config

def token_required(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Bearer '):
            return jsonify({'error': config.errorCodes[503]}), 403

        token = auth_header.split('Bearer ')[1]
        if token not in config.tokens:
            return jsonify({'error': config.errorCodes[503]}), 403

        return await f(*args, **kwargs)
    return decorated_function
