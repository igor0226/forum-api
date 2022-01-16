from aiohttp import web
from threading import Thread
from handlers.user import create_user, get_user, modify_user
from handlers.forum import create_forum, get_forum, get_all_users
from handlers.thread import create_thread, get_threads, make_thread_vote, get_thread_details, modify_thread
from handlers.post import create_posts, get_thread_posts, get_post, modify_post
from handlers.service import get_all_tables_count, clear_all_tables
from logger import app_logger
from perf_logger import perf_logger_worker, q


# TODO use fetchVal/fetchRow where it is possible
# TODO: close db socket before exiting app
# TODO: git hooks
# TODO: run flake8 and fix all errors
# TODO: make yaml config
# TODO: check SQL injections
# TODO: may be provide body from validate_json
# TODO: make own tests
# TODO: catch and log all project exceptions
# TODO: pep8 warnings
# TODO: docker-compose
# TODO: answers monitoring
# TODO: telegram notifications
# TODO: kubernetes
app = web.Application()
app.router.add_route('POST', '/api/user/{nickname}/create', create_user)
app.router.add_route('GET', '/api/user/{nickname}/profile', get_user)
app.router.add_route('POST', '/api/user/{nickname}/profile', modify_user)

app.router.add_route('POST', '/api/forum/create', create_forum)
app.router.add_route('GET', '/api/forum/{slug}/details', get_forum)

app.router.add_route('POST', '/api/forum/{slug}/create', create_thread)
app.router.add_route('GET', '/api/forum/{slug}/threads', get_threads)
app.router.add_route('GET', '/api/forum/{slug}/users', get_all_users)

app.router.add_route('POST', '/api/thread/{slug_or_id}/vote', make_thread_vote)
app.router.add_route('GET', '/api/thread/{slug_or_id}/details', get_thread_details)
app.router.add_route('POST', '/api/thread/{slug_or_id}/details', modify_thread)

app.router.add_route('POST', '/api/thread/{slug_or_id}/create', create_posts)
app.router.add_route('GET', '/api/thread/{slug_or_id}/posts', get_thread_posts)

app.router.add_route('GET', '/api/post/{id}/details', get_post)
app.router.add_route('POST', '/api/post/{id}/details', modify_post)

app.router.add_route('GET', '/api/service/status', get_all_tables_count)
app.router.add_route('POST', '/api/service/clear', clear_all_tables)

# perf logging
perf_logging_thread = Thread(
    target=perf_logger_worker,
    args=(q,),
)
perf_logging_thread.start()
perf_logging_thread.join()
# perf logging

app_logger.info('app started')
web.run_app(app, port=5000)
app_logger.info('app stopped')


