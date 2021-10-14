from aiohttp import web
from handlers.user import create_user, get_user, modify_user
from handlers.forum import create_forum

# TODO: make yaml config
# TODO: check SQL injections
# TODO: may be provide body from validate_json
# TODO: logging
app = web.Application()
app.router.add_route('POST', '/api/user/{nickname}/create', create_user)
app.router.add_route('GET', '/api/user/{nickname}/profile', get_user)
app.router.add_route('POST', '/api/user/{nickname}/profile', modify_user)

app.router.add_route('POST', '/api/forum/create', create_forum)

web.run_app(app, port=5000)
