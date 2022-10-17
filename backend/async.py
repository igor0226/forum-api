import asyncio
from time import time


async def sleep(delay: int):
    start_time = time()
    future = asyncio.Future()

    def wait():
        loop1 = asyncio.get_event_loop()
        if time() - start_time > delay:
            future.set_result('Hek')
        else:
            loop1.call_later(0, wait)

    wait()
    print('SLEEP')
    return await future


async def loop_func():
    await asyncio.wait([
        asyncio.ensure_future(sleep(2)),
        asyncio.ensure_future(sleep(2))
    ])
    print('HERE')


loop = None

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_func())
