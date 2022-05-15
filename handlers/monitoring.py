from aiohttp import web


async def ws_handler(req: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(req)

    async for msg in ws:
        # if msg.type == web.MsgType.text:
        print(msg)
        await ws.send_str("Hello, {}".format(msg.data))
        # elif msg.type == web.MsgType.binary:
        #     await ws.send_bytes(msg.data)
        # elif msg.type == web.MsgType.close:
        break

    return ws
