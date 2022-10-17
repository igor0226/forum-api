from aiohttp import web
import os
import asyncio
import json
from time import time

last_tick = time()
RPS_REPORT_FILE = os.path.join('log', 'rps', 'rps.json')


def read_rps_file():
    with open(RPS_REPORT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        return data


async def ws_handler(req: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    global last_tick

    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            rps_data = read_rps_file()
            await ws.send_json(data=rps_data)

            while not ws.closed:
                rps_list = read_rps_file()
                requests_num = 0 if not len(rps_list) else rps_list[len(rps_list) - 1]
                seconds_passed = time() - last_tick

                if seconds_passed < 1:
                    await asyncio.sleep(1 - seconds_passed)

                last_tick = time()

                try:
                    await ws.send_str(str(requests_num))
                except ConnectionResetError:
                    break
        elif msg.type == web.WSMsgType.close:
            break

    return ws
