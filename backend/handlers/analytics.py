import os
from aiohttp import web
from config import app_config
from handlers.helpers import (
    is_non_empty_file,
    aggregate_perf_report,
    validate_route_param,
)
from handlers.validators import not_null_str


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
            'description': endpoint['description'],
        })

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=body,
        headers=get_cors_headers(),
    )


async def get_perf_reports_list(_):
    log_dir = os.path.join(app_config['logs_dir'], 'perf')
    non_empty_files = list(filter(
        lambda f: is_non_empty_file(f, log_dir),
        os.listdir(log_dir),
    ))

    body = list()

    for report_file_name in list(non_empty_files):
        # duration-name.json -> name
        formatted_report_file = report_file_name[9:-5:]
        body.append(formatted_report_file)

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=body,
        headers=get_cors_headers(),
    )


@validate_route_param(
    name='report_id',
    validator=not_null_str,
)
async def get_perf_report(request: web.Request):
    report_id = request.match_info['report_id']
    report_file_name = 'duration-{}.json'.format(report_id)

    log_dir = os.path.join(app_config['logs_dir'], 'perf')
    full_report_file_name = os.path.join(log_dir, report_file_name)

    if not os.path.exists(full_report_file_name):
        return web.json_response(
            status=web.HTTPNotFound.status_code,
            data={'message': 'bad file'},
            headers=get_cors_headers(),
        )

    report_details = aggregate_perf_report(full_report_file_name)

    if not report_details:
        return web.json_response(
            status=web.HTTPNotFound.status_code,
            data={'message': 'bad file'},
            headers=get_cors_headers(),
        )

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=report_details,
        headers=get_cors_headers(),
    )
