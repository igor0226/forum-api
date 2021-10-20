from aiohttp import web
from handlers.user import create_user, get_user, modify_user
from handlers.forum import create_forum, get_forum
from handlers.thread import create_thread
from logger import app_logger


# TODO: make yaml config
# TODO: check SQL injections
# TODO: may be provide body from validate_json
# TODO: catch and log all project exceptions
app = web.Application()
app.router.add_route('POST', '/api/user/{nickname}/create', create_user)
app.router.add_route('GET', '/api/user/{nickname}/profile', get_user)
app.router.add_route('POST', '/api/user/{nickname}/profile', modify_user)

app.router.add_route('POST', '/api/forum/create', create_forum)
app.router.add_route('GET', '/api/forum/{slug}/details', get_forum)

app.router.add_route('POST', '/api/forum/{slug}/create', create_thread)

app_logger.info('app started')
web.run_app(app, port=5000)
app_logger.info('app stopped')
