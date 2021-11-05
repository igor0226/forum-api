from aiohttp import web
from .helpers import (
    validate_route_param,
    validate_query_params,
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
    is_bool_str,
)
from models.user import user_model
from models.forum import forum_model
from models.thread import thread_model


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
        validator=not_null_str,
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
    body = await request.json()
    forum_slug = body.get('forum') or request.match_info['slug']
    thread_slug = body.get('slug')
    thread_id = body.get('id')
    message = body.get('message')
    title = body.get('title')
    author = body.get('author')
    votes = body.get('votes') or 0
    created = body.get('created')

    found_users, error = await user_model.get_users(
        nickname=author,
    )

    if error:
        return response_with_error()

    found_forums, error = await forum_model.get_forum(
        slug=forum_slug,
    )

    if error:
        return response_with_error()

    if (
        not found_users or not len(found_users)
        or not found_forums or not len(found_forums)
    ):
        return web.json_response(
            data={'message': 'user or forum not found'},
            status=web.HTTPNotFound.status_code,
        )

    # TODO: make function for checking existing threads
    if thread_slug:
        found_threads, error = await thread_model.get_thread(
            slug=thread_slug,
            thread_id=thread_id,
        )
    
        if error:
            return response_with_error()
    
        for thread in found_threads:
            conflict_thread = thread_model.serialize(thread)
    
            return web.json_response(
                data=conflict_thread,
                status=web.HTTPConflict.status_code,
            )

    created_threads, error = await thread_model.insert_thread(
        author=author,
        forum=found_forums[0].get('slug'),
        message=message,
        title=title,
        votes=votes,
        created=created,
        thread_id=thread_id,
        slug=thread_slug,
    )

    if error:
        return response_with_error()

    created_thread = thread_model.serialize(created_threads[0])

    return web.json_response(
        data=created_thread,
        status=web.HTTPCreated.status_code,
    )


@add_logging()
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
        name='since',
        required=False,
        validator=is_timestamp,
    ),
    field(
        name='desc',
        required=False,
        validator=is_bool_str,
    ),
)
async def get_threads(request: web.Request):
    slug = request.match_info['slug']
    limit = request.query.get('limit')
    since = request.query.get('since')
    desc = request.query.get('desc')

    found_forums, error = await forum_model.get_forum(slug=slug)

    if error:
        return response_with_error()

    if not found_forums or not len(found_forums):
        return web.json_response(
            data={'message': 'forum not found'},
            status=web.HTTPNotFound.status_code,
        )

    found_threads, error = await thread_model.get_threads_by_forum(
        slug=slug,
        limit=limit,
        since=since,
        desc=desc,
    )

    if error:
        return response_with_error()

    threads_response = []

    for thread in found_threads:
        threads_response.append(
            thread_model.serialize(thread)
        )

    return web.json_response(
        data=threads_response,
        status=web.HTTPOk.status_code,
    )
