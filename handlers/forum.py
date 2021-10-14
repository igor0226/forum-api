from aiohttp import web
from models.forum import forum_model
from .helpers import field, validate_json, response_with_error
from .validators import is_non_negative, is_nickname, is_url


# TODO: validate url with re
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
        validator=is_url,
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
    posts = body.get('posts')
    slug = body.get('slug')
    threads = body.get('threads')
    title = body.get('title')
    author = body.get('user')

    found_forum, error = await forum_model.get_forum(slug=slug)

    if error:
        return response_with_error()

    for forum in found_forum:
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
