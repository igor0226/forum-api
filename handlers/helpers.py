import re
import os
import json
import math
from typing import Dict
from time import time
from json import decoder
from aiohttp import web
from handlers.validators import default_validator
from logger import app_logger
from perf.perf_logger import q
from perf.rps_queue import rps_queue

api_param_reg_exp = re.compile('^/api/[^/]+/([^/]+)/[^/]+$')


def _get_url_key(url, method):
    prefix_index = url.find('/api')
    cut_url = url[prefix_index::]
    match = api_param_reg_exp.match(cut_url)

    if match:
        param = match.group(1)
        param_beg_index = cut_url.find(param)
        param_end_index = param_beg_index + len(param)
        cut_url = cut_url[0:param_beg_index - 1:] + cut_url[param_end_index::]

    query_separator = cut_url.find('?')

    if query_separator != -1:
        cut_url = cut_url[:query_separator - 1:]

    return '{}:{}'.format(cut_url, method)


def add_logging(handler):
    async def inner(request: web.Request):
        rps_queue.append('new request')
        body = await request.text()
        app_logger.info('GOT {} {}, body: {}'.format(
            request.method,
            request.rel_url,
            body,
        ))

        beg_time = time()
        response = await handler(request)
        q.put((
            _get_url_key(str(request.url), request.method),
            time() - beg_time,
        ))

        return response

    return inner


def response_with_error():
    return web.json_response(
        data={'message': 'Internal server error'},
        status=web.HTTPInternalServerError.status_code,
    )


def _validate_field(field_dict, value_to_validate):
    required = field_dict.get('required')
    field_type = field_dict.get('field_type')
    validator = field_dict.get('validator')
    
    has_value = value_to_validate is not None
    
    return not (
        required and not has_value or
        has_value and type(value_to_validate) != field_type or
        has_value and not validator(value_to_validate)
    )


def validate_query_params(*fields: Dict):
    def wrapper(handler):
        async def inner(request: web.Request):
            for field_dict in fields:
                name = field_dict.get('name')
                value_to_validate = request.query.get(name)
                is_valid = _validate_field(field_dict, value_to_validate)

                if not is_valid:
                    app_logger.info('Query validating failure for {} in {}'.format(
                        request.rel_url,
                        name,
                    ))
    
                    return web.json_response(
                        data={'message': 'query param validating failure for "{}"'.format(name)},
                        status=web.HTTPUnprocessableEntity.status_code,
                    )

            return await handler(request)

        return inner

    return wrapper


def validate_route_param(name, validator):
    def wrapper(handler):
        async def inner(request: web.Request):
            param = request.match_info.get(name)

            if not param or not validator(param):
                app_logger.info('Route param validating failure for {} in {}'.format(
                    request.rel_url,
                    name,
                ))
                return web.json_response(
                    data={'message': 'bad route parameter'},
                    status=web.HTTPUnprocessableEntity.status_code,
                )

            return await handler(request)

        return inner

    return wrapper


def field(name: str, required: bool,
          field_type=str, validator=default_validator):
    return {
        'name': name,
        'required': required,
        'field_type': field_type,
        'validator': validator,
    }


async def safe_parse_json(request):
    body = None
    error = False

    try:
        body = await request.json()
    except decoder.JSONDecodeError:
        text = await request.text()
        app_logger.info('JSON decoding error for {} got {}'.format(
            request.rel_url,
            text,
        ))
        error = True
    finally:
        return body, error


def validate_json(*fields: Dict):
    def wrapper(handler):
        async def inner(request: web.Request):
            body, error = await safe_parse_json(request)
            if error:
                return web.json_response(
                    data={'message': 'wrong request body format'},
                    status=web.HTTPBadRequest.status_code,
                )

            array_body = isinstance(body, list)

            for val in (body if array_body else [body]):
                for field_dict in fields:
                    name = field_dict.get('name')
                    value_to_validate = val.get(name)
                    is_valid = _validate_field(field_dict, value_to_validate)

                    if not is_valid:
                        text = await request.text()
                        app_logger.info('JSON validating failure for {} got {}'.format(
                            request.rel_url,
                            text,
                        ))

                        return web.json_response(
                            data={'message': 'wrong request body format in field "{}"'.format(name)},
                            status=web.HTTPUnprocessableEntity.status_code,
                        )

            return await handler(request)

        return inner

    return wrapper


def is_non_empty_file(file, dir_name):
    file_name = os.path.join(dir_name, file)

    return bool(os.path.getsize(file_name))


def _format_duration(duration):
    return round(duration, 5)


def _get_percentile(data, percentile):
    data_len = len(data)
    return _format_duration(data[math.floor(data_len * percentile / 100)])


def aggregate_perf_report(report_file):
    report = dict()

    try:
        with open(report_file) as f:
            report_lines = json.load(f)
            for report_line in report_lines:
                for path_key in report_line:
                    durations = report.get(path_key) or []
                    durations.append(report_line.get(path_key))
                    report.update({path_key: durations})
    except OSError:
        return None

    percentiles = list()

    # percentiles
    for path_key in report:
        durations = report.get(path_key)
        durations.sort()

        perc_list = list()
        perc_list.append({
            'name': '10 percentile',
            'value': _get_percentile(durations, 10)
        })
        perc_list.append({
            'name': '25 percentile',
            'value': _get_percentile(durations, 25)
        })
        perc_list.append({
            'name': '50 percentile',
            'value': _get_percentile(durations, 50)
        })
        perc_list.append({
            'name': '75 percentile',
            'value': _get_percentile(durations, 75)
        })
        perc_list.append({
            'name': '90 percentile',
            'value': _get_percentile(durations, 90)
        })

        (path, method) = path_key.split(':')
        percentiles.append({
            'key': path_key,
            'path': path,
            'method': method,
            'percentiles': perc_list,
        })

    return percentiles

