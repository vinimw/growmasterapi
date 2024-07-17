import aiohttp
import ssl
import logging
from quart import jsonify
from urllib.parse import urlencode
import config

async def fetch_external_data(url, headers=None):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    conn = aiohttp.TCPConnector(ssl=ssl_context)
    try:
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(url, headers=headers) as response:
                logging.debug(f"Response status: {response.status}")
                if response.status == 200:
                    return await response.json(), 200
                else:
                    return {'error': config.errorCodes[701]}, response.status
    except aiohttp.ClientError as e:
        logging.error(f"Client error: {str(e)}")
        return {'error': str(e)}, 500

def build_request_params(endpoint, query_params):
    base_url = config.endpoints[endpoint]
    url = f"{base_url}?{urlencode(query_params)}"
    headers = {"x-client-id": config.clientId}
    return url, headers

def build_request_params_post(endpoint, query_params=None):
    base_url = config.endpoints[endpoint]
    url = base_url
    headers = {"x-client-id": config.clientId}
    return url, headers


async def post_external_data(url, data, headers=None):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    conn = aiohttp.TCPConnector(ssl=ssl_context)
    try:
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.post(url, json=data, headers=headers) as response:
                logging.debug(f"Response status: {response.status}")
                if response.status == 200:
                    return await response.json(), 200
                else:
                    return {'error': config.errorCodes[701]}, response.status
    except aiohttp.ClientError as e:
        logging.error(f"Client error: {str(e)}")
        return {'error': str(e)}, 500
