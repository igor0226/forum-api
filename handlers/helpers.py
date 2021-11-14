from typing import Dict, List
from functools import reduce
from json import decoder
from aiohttp import web
from handlers.validators import default_validator
from logger import app_logger


def add_logging(handler):
    async def inner(request: web.Request):
        body = await request.text()
        app_logger.info('GOT {} {}, body: {}'.format(
            request.method,
            request.rel_url,
            body,
        ))

        return await handler(request)

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


def dict_from_list(values_list, key):
    def unique_appender(values_dict, value):
        got_by_key = value.get(key)
        if got_by_key and got_by_key not in values_dict:
            values_dict[got_by_key] = True

        return values_dict

    return reduce(unique_appender, values_list, dict())
