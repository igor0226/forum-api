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
            data={'message': 'user or forum not found'}
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
            conflict_thread = {
                'id': thread.get('id'),
                'author': thread.get('author'),
                # 'created': thread.get('created'),
                'forum': thread.get('forum'),
                'message': thread.get('message'),
                'slug': thread.get('slug'),
                'title': thread.get('title'),
                'votes': thread.get('votes'),
            }
    
            return web.json_response(
                data=conflict_thread,
                status=web.HTTPConflict.status_code,
            )

    created_threads, error = await thread_model.insert_thread(
        author=author,
        forum=forum_slug,
        message=message,
        title=title,
        votes=votes,
        created=created,
        thread_id=thread_id,
        slug=thread_slug,
    )

    if error:
        return response_with_error()

    created_thread = {
        'id': created_threads[0].get('id'),
        'author': created_threads[0].get('author'),
        # 'created': created_threads[0].get('created'),
        'forum': created_threads[0].get('forum'),
        'message': created_threads[0].get('message'),
        'slug': created_threads[0].get('slug'),
        'title': created_threads[0].get('title'),
        'votes': created_threads[0].get('votes'),
    }

    return web.json_response(
        data=created_thread,
        status=web.HTTPCreated.status_code,
    )
