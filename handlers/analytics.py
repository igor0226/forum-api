from aiohttp import web
from config import app_config


def get_cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type',
    }


async def options_prefetch(_):
    return web.HTTPOk(headers=get_cors_headers())


async def get_endpoints(_):
    body = []

    for endpoint_name in app_config['endpoints']:
        endpoint = app_config['endpoints'][endpoint_name]
        body.append({
            'method': endpoint['method'],
            'path': endpoint['path'],
        })

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=body,
        headers=get_cors_headers(),
    )
