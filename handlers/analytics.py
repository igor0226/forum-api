from aiohttp import web
import os
import pathlib
import json
from config import app_config
from handlers.helpers import is_non_empty_file, aggregate_perf_report


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

    non_empty_files = list(filter(
        lambda f: is_non_empty_file(f, log_dir),
        os.listdir(log_dir),
    ))

    body = dict()

    for report_file_name in list(non_empty_files):
        report_file = os.path.join(log_dir, report_file_name)
        report_data = aggregate_perf_report(report_file)
        # duration-name.json -> name
        formatted_report_file = 'Report #{}'.format(report_file_name[9:-5:])
        body.update({formatted_report_file: report_data})

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=body,
        headers=get_cors_headers(),
    )
