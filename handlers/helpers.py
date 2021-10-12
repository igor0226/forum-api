from typing import Dict
from json import decoder
from aiohttp import web
from .validators import default_validator


def response_with_error():
    return web.json_response(
        data={'message': 'Internal server error'},
        status=web.HTTPInternalServerError.status_code,
    )


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
                return web.json_response(
                    data={'message': 'wrong request body format'},
                    status=web.HTTPBadRequest.status_code,
                )

            for field_dict in fields:
                name = field_dict.get('name')
                required = field_dict.get('required')
                field_type = field_dict.get('field_type')
                validator = field_dict.get('validator')

                value_from_body = body.get(name)
                has_value = value_from_body is not None

                is_invalid = (
                        required and not has_value or
                        has_value and type(value_from_body) != field_type or
                        has_value and not validator(value_from_body)
                )

                if is_invalid:
                    return web.json_response(
                        data={'message': 'wrong request body format in field "{}"'.format(name)},
                        status=web.HTTPUnprocessableEntity.status_code,
                    )

            return await handler(request)

        return inner

    return wrapper