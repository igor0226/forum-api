from aiohttp import web
from handlers.helpers import (
    field,
    add_logging,
    validate_json,
    validate_route_param,
    validate_query_params,
    response_with_error,
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
    is_string_enum,
)
from models.post import post_model
from models.thread import thread_model
from models.user import user_model
from asyncio import sleep


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

    posts_authors = set(map(lambda p: p.get('author'), posts))
    flags, error = await user_model.check_users_nicknames(
        nicknames=posts_authors,
    )

    if error:
        return response_with_error()

    authors_exists = flags[0].get('authors_exists')
    if not authors_exists:
        return web.json_response(
            status=web.HTTPNotFound.status_code,
            data={'message': 'check posts authors'}
        )

    thread_id = found_threads[0].get('id')
    parent_post_ids = set(map(lambda p: p.get('parent'), posts))
    post_ids = set(map(lambda p: p.get('id'), posts))
    existing_parent_posts_ids = list(set(parent_post_ids) - set(post_ids))
    flags, error = await post_model.check_posts_to_create(
        parent_post_ids=existing_parent_posts_ids,
        thread_id=thread_id,
    )

    if error:
        return response_with_error()

    is_valid = flags[0].get('posts_are_valid')
    if not is_valid:
        return web.json_response(
            status=web.HTTPConflict.status_code,
            data={'message': 'check posts parent ids'}
        )

    if not len(posts):
        return web.json_response(
            data=[],
            status=web.HTTPCreated.status_code,
        )

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
        validator=is_non_negative,
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
    sort = request.query.get('sort') or 'flat'
    desc = request.query.get('desc') == 'true'
    thread_id = found_threads[0].get('id')
    since_path = None
    limit_root = None

    if since is not None and sort != 'flat':
        last_posts, error = await post_model.get_post(post_id=since)

        if error:
            return response_with_error()

        if len(last_posts):
            since_path = last_posts[0].get('pathArray'.lower())

    if limit is not None and sort == 'parent_tree':
        last_posts, error = await post_model.get_parent_threads(
            thread_id=thread_id,
            limit=limit,
            desc=desc,
            since_path=since_path,
        )

        if error:
            return response_with_error()

        last_posts_len = len(last_posts)

        if last_posts_len:
            limit_root = last_posts[last_posts_len - 1].get('id')

            if not desc:
                limit_root += 1
            elif desc:
                limit_root -= 1

        else:
            limit_root = 0

    found_posts, error = await post_model.get_thread_posts(
        thread_id=thread_id,
        limit=limit,
        sort=sort,
        desc=desc,
        since=since,
        since_path=since_path,
        limit_root=limit_root,
    )

    if error:
        return response_with_error()

    posts_answer = []

    for post in found_posts:
        posts_answer.append(
            post_model.serialize(post),
        )

    return web.json_response(
        data=posts_answer,
        status=web.HTTPOk.status_code,
    )


@add_logging
@validate_route_param(
    name='id',
    validator=is_non_negative
)
@validate_query_params(
    field(
        name='related',
        required=False,
        validator=is_string_enum('user', 'thread', 'forum')
    ),
)
async def get_post(request: web.Request):
    post_id = request.match_info['id']
    related_fields = request.query.get('related', '')
    found_posts, error = await post_model.get_related_info(post_id)

    if error:
        return response_with_error()

    if not found_posts or not len(found_posts):
        return web.json_response(
            status=web.HTTPNotFound.status_code,
            data={'message': 'post not found'}
        )

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=post_model.serialize_related_info(
            db_object=found_posts[0],
            author='user' in related_fields,
            forum='forum' in related_fields,
            thread='thread' in related_fields,
        )
    )


@add_logging
@validate_route_param(
    name='id',
    validator=is_non_negative
)
@validate_json(
    field(
        name='created',
        required=False,
        field_type=str,
        validator=is_timestamp,
    ),
    field(
        name='message',
        required=False,
        field_type=str,
        validator=not_null_str,
    ),
)
async def modify_post(request: web.Request):
    post_id = request.match_info['id']
    post_update = await request.json()
    created = post_update.get('created')
    message = post_update.get('message')
    is_empty_update = not created and not message

    found_posts, error = await post_model.get_post(post_id=post_id)

    if error:
        return response_with_error()

    if not found_posts or not len(found_posts):
        return web.json_response(
            status=web.HTTPNotFound.status_code,
            data={'message': 'post not found'},
        )

    if is_empty_update:
        return web.json_response(
            status=web.HTTPOk.status_code,
            data=post_model.serialize(found_posts[0]),
        )

    updated_posts, error = await post_model.modify_post(
        post_id=post_id,
        message=message,
        created=created,
    )

    if error:
        return response_with_error()

    return web.json_response(
        status=web.HTTPOk.status_code,
        data=post_model.serialize(updated_posts[0]),
    )
