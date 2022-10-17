from aiohttp import web
from handlers.helpers import add_logging, response_with_error
from models.service import service_model


@add_logging
async def get_all_tables_count(request: web.Request):
    service_status, error = await service_model.get_all_tables_count()

    if error:
        return response_with_error()

    return web.json_response(
        data=service_model.serialize(service_status[0]),
        status=web.HTTPOk.status_code,
    )


@add_logging
async def clear_all_tables(request: web.Request):
    _, error = await service_model.clear_all_tables()

    if error:
        return response_with_error()

    return web.Response(status=web.HTTPOk.status_code)
