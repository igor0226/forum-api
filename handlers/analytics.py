from aiohttp import web
import os
import pathlib
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


async def get_perf_reports_list(_):
    log_dir = os.path.join(
        pathlib.Path(__file__).parent.parent.resolve(),
        'log',
        'perf',
    )

    body = list(map(lambda f: f[9:-5:], os.listdir(log_dir)))

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=body,
        headers=get_cors_headers(),
    )
