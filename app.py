from aiohttp import web
from handlers.user import create_user, get_user, modify_user
from handlers.forum import create_forum, get_forum
from handlers.thread import create_thread, get_threads, make_thread_vote, get_thread_details
from handlers.post import create_posts, get_thread_posts, get_post
from logger import app_logger


# TODO use fetchVal/fetchRow where it is possible
# TODO: close db socket before exiting app
# TODO: git hooks
# TODO: more smart templates for SQL
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

app.router.add_route('POST', '/api/thread/{slug_or_id}/vote', make_thread_vote)
app.router.add_route('GET', '/api/thread/{slug_or_id}/details', get_thread_details)

app.router.add_route('POST', '/api/thread/{slug_or_id}/create', create_posts)
app.router.add_route('GET', '/api/thread/{slug_or_id}/posts', get_thread_posts)

app.router.add_route('GET', '/api/post/{id}/details', get_post)

app_logger.info('app started')
web.run_app(app, port=5000)
app_logger.info('app stopped')
