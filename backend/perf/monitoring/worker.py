import os.path
import json
from time import time
from config import app_config

RPS_REPORT_FILE = os.path.join(
    app_config['logs_dir'],
    'rps',
    'rps.json',
)
rps_list = []
MAX_RPS_LIST_LENGTH = 50


def dump_rps():
    with open(RPS_REPORT_FILE, 'w') as f:
        json.dump(rps_list, f, indent=4)


def perf_monitoring_worker(rps_queue):
    last_tick = time()
    global rps_list

    while True:
        if time() - last_tick > 1:
            last_tick = time()
        else:
            continue

        rps_list.append(rps_queue.qsize())
        dump_rps()

        if len(rps_list) > MAX_RPS_LIST_LENGTH:
            start = len(rps_list) - MAX_RPS_LIST_LENGTH
            rps_list = rps_list[start:]

        while not rps_queue.empty():
            rps_queue.get()
