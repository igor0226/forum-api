from aiohttp import web
from models.user import user_model
from .helpers import field, validate_json, response_with_error
from .validators import not_null_str


# TODO validate email and nickname with re
@validate_json(
    field(
        name='about',
        required=False,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='email',
        required=True,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='nickname',
        required=True,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='fullname',
        required=False,
        field_type=str,
        validator=not_null_str,
    ),
)
async def create_user(request: web.Request):
    body = await request.json()

    nickname = request.match_info['nickname']
    about = body.get('about')
    email = body.get('email')
    fullname = body.get('fullname')

    existing_users, error = await user_model.get_users(
        nickname=nickname,
        email=email,
    )

    if error:
        return response_with_error()

    if existing_users:
        response_body = []
        for user in existing_users:
            response_body.append({
                about: user.get('about'),
                email: user.get('email'),
                nickname: user.get('nickname'),
                fullname: user.get('fullname'),
            })
    
        return web.json_response(
            data=response_body,
            status=web.HTTPConflict.status_code,
        )

    users_list, error = await user_model.insert(
        about=about,
        nickname=nickname,
        email=email,
        fullname=fullname,
    )

    if error:
        return response_with_error()

    response_body = {}

    for user in users_list:
        response_body = {
            'about': user.get('about'),
            'email': user.get('email'),
            'fullname': user.get('fullname'),
            'nickname': user.get('nickname'),
        }

    return web.json_response(
        data=response_body,
        status=web.HTTPCreated.status_code,
    )


async def get_user(request: web.Request):
    nickname = request.match_info['nickname']

    found_users, error = await user_model.get_users(nickname=nickname)

    if error:
        response_with_error()

    if not found_users or not len(found_users):
        return web.json_response(
            data={'message': 'user not found'},
            status=web.HTTPNotFound.status_code,
        )

    response_body = {}

    for user in found_users:
        response_body = {
            'about': user.get('about'),
            'email': user.get('email'),
            'fullname': user.get('fullname'),
            'nickname': user.get('nickname'),
        }

    return web.json_response(
        data=response_body,
        status=web.HTTPOk.status_code,
    )


@validate_json(
    field(
        name='about',
        required=False,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='email',
        required=False,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='fullname',
        required=False,
        field_type=str,
        validator=not_null_str,
    ),
)
async def modify_user(request: web.Request):
    nickname = request.match_info['nickname']

    found_users, error = await user_model.get_users(nickname=nickname)

    if error:
        return response_with_error()

    if not found_users or not len(found_users):
        return web.json_response(
            data={'message': 'user does not exist'},
            status=web.HTTPNotFound.status_code,
        )

    return response_with_error()
