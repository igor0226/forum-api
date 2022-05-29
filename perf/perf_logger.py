import os
import pathlib
import json
from time import time
from queue import Queue
from datetime import datetime
from perf.rps_queue import rps_queue


class PerfLogger:
    def __init__(self):
        log_dir = os.path.join(
            pathlib.Path(__file__).parent.resolve(),
            '../log',
        )
        log_inner_dir = os.path.join(
            log_dir,
            'perf',
        )
        cur_date = datetime.now()
        log_file_name = 'duration-{}.{}.{}-{}:{}.json'.format(
            cur_date.day,
            cur_date.month,
            cur_date.year,
            cur_date.hour,
            cur_date.minute,
        )
        self.log_file = os.path.join(
            log_inner_dir,
            log_file_name,
        )

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        if not os.path.exists(log_inner_dir):
            os.mkdir(log_inner_dir)

        self.log_file_created = False

    def write_duration(self, key, duration):
        if not self.log_file_created:
            if not os.path.exists(self.log_file):
                open(self.log_file, 'w')

            self.log_file_created = True

        with open(self.log_file, 'r') as f:
            try:
                data = json.load(f) or []
            except json.JSONDecodeError:
                data = []

            with open(self.log_file, 'w') as empty_file:
                data.append({
                    str(key): duration
                })
                json.dump(data, empty_file, indent=4)


q = Queue()


def perf_logger_worker(observations_queue):
    perf_logger = PerfLogger()

    while True:
        (key, duration) = observations_queue.get()
        perf_logger.write_duration(key, duration)
        # observations_queue.task_done()


rps_list = []
MAX_RPS_LIST_LENGTH = 50


def monitoring_worker():
    last_tick = time()
    global rps_list

    while True:
        if time() - last_tick > 1:
            last_tick = time()
        else:
            continue

        rps_list.append(len(rps_queue))

        if len(rps_list) > MAX_RPS_LIST_LENGTH:
            start = len(rps_list) - MAX_RPS_LIST_LENGTH
            rps_list = rps_list[start:]

        rps_queue.clear()

