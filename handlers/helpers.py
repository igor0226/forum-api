from typing import Dict
from json import decoder
from aiohttp import web
from .validators import default_validator
from logger import app_logger


def add_logging():
    def wrapper(handler):
        async def inner(request: web.Request):
            body = await request.text()
            app_logger.info('GOT {} {}, body: {}'.format(request.method, request.rel_url, body))

            return await handler(request)

        return inner

    return wrapper


def response_with_error():
    return web.json_response(
        data={'message': 'Internal server error'},
        status=web.HTTPInternalServerError.status_code,
    )


def validate_route_param(name, validator):
    def wrapper(handler):
        async def inner(request: web.Request):
            param = request.match_info.get(name)

            if not param or not validator(param):
                return web.json_response(
                    data={'message': 'bad route parameter'},
                    status=web.HTTPUnprocessableEntity.status_code,
                )

            return await handler(request)

        return inner

    return wrapper


def field(name: str, required: bool, field_type=str, validator=default_validator):
    return {
        'name': name,
        'required': required,
        'field_type': field_type,
        'validator': validator,
    }


def validate_json(*fields: Dict):
    def wrapper(handler):
        async def inner(request: web.Request):
            try:
                body = await request.json()
            except decoder.JSONDecodeError:
                text = await request.text()
                app_logger.info('JSON decoding error for {} got {}'.format(request.rel_url, text))
                return web.json_response(
                    data={'message': 'wrong request body format'},
                    status=web.HTTPBadRequest.status_code,
                )

            for field_dict in fields:
                name = field_dict.get('name')
                required = field_dict.get('required')
                field_type = field_dict.get('field_type')
                validator = field_dict.get('validator')

                value_to_validate = body.get(name)
                has_value = value_to_validate is not None

                is_invalid = (
                        required and not has_value or
                        has_value and type(value_to_validate) != field_type or
                        has_value and not validator(value_to_validate)
                )

                if is_invalid:
                    text = await request.text()
                    app_logger.info('JSON validating failure for {} got {}'.format(request.rel_url, text))

                    return web.json_response(
                        data={'message': 'wrong request body format in field "{}"'.format(name)},
                        status=web.HTTPUnprocessableEntity.status_code,
                    )

            return await handler(request)

        return inner

    return wrapper
