from aiohttp import web
from handlers.user import create_user, get_user, modify_user

# TODO: yaml with config
app = web.Application()
app.router.add_route('POST', '/api/{nickname}/create', create_user)
app.router.add_route('GET', '/api/{nickname}/profile', get_user)
app.router.add_route('POST', '/api/{nickname}/profile', modify_user)

web.run_app(app, port=5000)
