from aiohttp import web
from .helpers import (
    validate_route_param,
    validate_json,
    add_logging,
    field,
    response_with_error,
)
from .validators import (
    is_non_digit,
    is_nickname,
    not_null_str,
    is_non_negative,
    is_timestamp,
)


@add_logging()
@validate_route_param(
    name='slug',
    validator=is_non_digit,
)
@validate_json(
    field(
        name='slug',
        required=False,
        field_type=str,
        validator=is_non_digit,
    ),
    field(
        name='forum',
        required=False,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='id',
        required=False,
        field_type=int,
        validator=is_non_negative,
    ),
    field(
        name='message',
        required=True,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='title',
        required=True,
        field_type=str,
    ),
    field(
        name='author',
        required=True,
        field_type=str,
        validator=is_nickname,
    ),
    field(
        name='votes',
        required=False,
        field_type=int,
        validator=is_non_negative,
    ),
    field(
        name='created',
        required=False,
        field_type=str,
        validator=is_timestamp,
    ),
)
async def create_thread(request: web.Request):
    return response_with_error()
