from aiohttp import web
from models.forum import forum_model
from models.user import user_model
from .helpers import field, validate_json, response_with_error, add_logging
from .validators import is_non_negative, is_nickname


@add_logging()
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
            response_body = {
                'posts': forum.get('posts'),
                'slug': forum.get('slug'),
                'threads': forum.get('threads'),
                'title': forum.get('title'),
                'user': forum.get('author'),
            }

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

    created_forums, error = await forum_model.create_forum(
        slug=slug,
        title=title,
        author=author,
        posts=posts,
        threads=threads,
    )

    if error:
        return response_with_error()

    response_body = {}

    for forum in created_forums:
        response_body = {
            'posts': forum.get('posts'),
            'slug': forum.get('slug'),
            'threads': forum.get('threads'),
            'title': forum.get('title'),
            'user': forum.get('author'),
        }

    return web.json_response(
        data=response_body,
        status=web.HTTPCreated.status_code
    )
