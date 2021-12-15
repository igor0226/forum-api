from aiohttp import web
from models.forum import forum_model
from models.user import user_model
from handlers.helpers import (
    field,
    validate_route_param,
    validate_query_params,
    validate_json,
    response_with_error,
    add_logging,
)
from handlers.validators import (
    is_non_negative,
    is_nickname,
    is_non_digit,
    is_bool_str,
    not_null_str,
)


@add_logging
@validate_json(
    field(
        name='posts',
        required=False,
        field_type=int,
        validator=is_non_negative,
    ),
    field(
        name='slug',
        required=True,
        field_type=str,
        validator=is_non_digit,
    ),
    field(
        name='threads',
        required=False,
        field_type=int,
        validator=is_non_negative,
    ),
    field(
        name='title',
        required=True,
        field_type=str,
    ),
    field(
        name='user',
        required=True,
        field_type=str,
        validator=is_nickname,
    ),
)
async def create_forum(request: web.Request):
    body = await request.json()
    posts = body.get('posts', 0)
    slug = body.get('slug')
    threads = body.get('threads', 0)
    title = body.get('title')
    author = body.get('user')

    found_forums, error = await forum_model.get_forum(slug=slug)

    if error:
        return response_with_error()

    if found_forums and len(found_forums):
        for forum in found_forums:
            response_body = forum_model.serialize(forum)

            return web.json_response(
                data=response_body,
                status=web.HTTPConflict.status_code,
            )

    found_users, error = await user_model.get_users(nickname=author)

    if not found_users or not len(found_users):
        return web.json_response(
            data={'message': 'user not found'},
            status=web.HTTPNotFound.status_code,
        )

    original_case_nickname = found_users[0].get('nickname')
    created_forums, error = await forum_model.create_forum(
        slug=slug,
        title=title,
        author=original_case_nickname,
        posts=posts,
        threads=threads,
    )

    if error:
        return response_with_error()

    response_body = forum_model.serialize(created_forums[0])

    return web.json_response(
        data=response_body,
        status=web.HTTPCreated.status_code
    )


@add_logging
@validate_route_param(
    name='slug',
    validator=is_non_digit,
)
async def get_forum(request: web.Request):
    slug = request.match_info['slug']

    found_forums, error = await forum_model.get_forum(slug=slug)

    if error:
        return response_with_error()

    if not found_forums or not len(found_forums):
        return web.json_response(
            data={'message': 'forum not found'},
            status=web.HTTPNotFound.status_code,
        )

    response_body = forum_model.serialize(found_forums[0])

    return web.json_response(
        data=response_body,
        status=web.HTTPOk.status_code,
    )


@add_logging
@validate_route_param(
    name='slug',
    validator=is_non_digit,
)
@validate_query_params(
    field(
        name='limit',
        required=False,
        validator=is_non_negative,
    ),
    field(
        name='desc',
        required=False,
        validator=is_bool_str,
    ),
    field(
        name='since',
        required=False,
        validator=not_null_str,
    ),
)
async def get_all_users(request: web.Request):
    slug = request.match_info['slug']
    limit = request.query.get('limit')
    since = request.query.get('since')
    desc = request.query.get('desc') == 'true'

    found_forums, error = await forum_model.get_forum(slug=slug)

    if error:
        return response_with_error()

    if not found_forums or not len(found_forums):
        return web.json_response(
            status=web.HTTPNotFound.status_code,
            data={'message': 'forum not found'}
        )

    found_users, error = await forum_model.get_all_users(
        slug=slug,
        limit=limit,
        since=since,
        desc=desc,
    )

    if error:
        return response_with_error()

    users_list = list(map(lambda user: user_model.serialize(user), found_users))

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=users_list,
    )
