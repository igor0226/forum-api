from aiohttp import web
from perf.perf_logger import get_rps_list
import asyncio
from time import time

last_tick = time()


async def ws_handler(req: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    global last_tick

    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            rps_list = get_rps_list()
            await ws.send_json(data=rps_list)

            while not ws.closed:
                rps_list = get_rps_list()
                requests_num = 0 if not len(rps_list) else rps_list[len(rps_list) - 1]
                seconds_passed = time() - last_tick

                if seconds_passed < 1:
                    await asyncio.sleep(1 - seconds_passed)

                last_tick = time()

                print('REQ', rps_list)
                try:
                    await ws.send_str(str(requests_num))
                except ConnectionResetError:
                    break
        elif msg.type == web.WSMsgType.close:
            break

    return ws
