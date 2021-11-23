from aiohttp import web
from handlers.helpers import (
    field,
    add_logging,
    validate_json,
    validate_route_param,
    validate_query_params,
    response_with_error,
    dict_from_list,
)
from handlers.validators import (
    some,
    not_null_str,
    is_digit,
    is_nickname,
    is_timestamp,
    is_non_digit,
    is_non_negative,
    is_bool_str,
    one_of,
)
from models.post import post_model
from models.thread import thread_model


@add_logging
@validate_route_param(
    name='slug_or_id',
    validator=some(
        is_non_digit,
        is_non_negative,
    ),
)
@validate_json(
    field(
        name='author',
        required=True,
        field_type=str,
        validator=is_nickname,
    ),
    field(
        name='created',
        required=False,
        field_type=str,
        validator=is_timestamp,
    ),
    field(
        name='forum',
        required=False,
        field_type=str,
        validator=is_non_digit,
    ),
    field(
        name='id',
        required=False,
        field_type=int,
        validator=is_non_negative,
    ),
    field(
        name='isEdited',
        required=False,
        field_type=str,
        validator=is_bool_str
    ),
    field(
        name='message',
        required=True,
        field_type=str,
        validator=not_null_str,
    ),
    field(
        name='parent',
        required=False,
        field_type=int,
        validator=is_non_negative,
    ),
    field(
        name='thread',
        required=False,
        field_type=int,
        validator=is_non_negative,
    ),
)
async def create_posts(request: web.Request):
    posts = await request.json()
    if not len(posts):
        return web.json_response(
            data=[],
            status=web.HTTPCreated.status_code,
        )

    parent_post_ids = dict_from_list(
        values_list=posts,
        key='parent',
    )
    post_ids = dict_from_list(
        values_list=posts,
        key='id',
    )
    not_found_post_ids, error = await post_model.get_non_existing_posts(
        post_ids=parent_post_ids,
    )

    if error:
        return response_with_error()

    not_found_post_ids = set(not_found_post_ids)
    post_ids = set(post_ids)
    for not_found_post_id in not_found_post_ids:
        if not not_found_post_id not in post_ids:
            return web.json_response(
                data={'message': 'parent post not found'},
                status=web.HTTPConflict.status_code,
            )

    thread_slug_or_id = request.match_info['slug_or_id']
    thread_id = int(thread_slug_or_id) if is_digit(thread_slug_or_id) else None
    found_threads, error = await thread_model.get_thread(
        slug=thread_slug_or_id,
        thread_id=thread_id,
    )

    if error:
        return response_with_error()

    if not found_threads or not len(found_threads):
        return web.json_response(
            data={'message': 'thread not found'},
            status=web.HTTPNotFound.status_code,
        )

    thread_id = found_threads[0].get('id')
    post_forum = found_threads[0].get('forum')
    created_posts, error = await post_model.create_posts(
        posts=posts,
        thread_id=thread_id,
        forum_slug=post_forum,
    )
    if error:
        return response_with_error()

    response_body = []
    for post in created_posts:
        response_body.append(post_model.serialize(
            db_object=post,
        ))

    return web.json_response(
        data=response_body,
        status=web.HTTPCreated.status_code,
    )


@add_logging
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
        name='sort',
        required=False,
        validator=one_of('flat', 'tree', 'parent_tree'),
    ),
    field(
        name='desc',
        required=False,
        validator=is_bool_str,
    ),
)
@validate_route_param(
    name='slug_or_id',
    validator=some(
        is_non_digit,
        is_non_negative,
    ),
)
async def get_thread_posts(request: web.Request):
    thread_slug_or_id = request.match_info['slug_or_id']
    thread_id = int(thread_slug_or_id) if is_digit(thread_slug_or_id) else None
    found_threads, error = await thread_model.get_thread(
        slug=thread_slug_or_id,
        thread_id=thread_id,
    )

    if error:
        return response_with_error()

    if not found_threads or not len(found_threads):
        return web.json_response(
            data={'message': 'thread not found'},
            status=web.HTTPNotFound.status_code,
        )

    limit = request.query.get('limit')
    since = request.query.get('since')
    sort = request.query.get('sort')
    desc = request.query.get('desc')
    thread_id = found_threads[0].get('id')

    found_posts, error = await post_model.get_thread_posts(
        thread_id=thread_id,
        limit=limit,
    )

    if error:
        return response_with_error()

    posts_answer = []
    for post in found_posts:
        posts_answer.append(
            post_model.serialize(post)
        )

    return web.json_response(
        data=posts_answer,
        status=web.HTTPOk.status_code,
    )