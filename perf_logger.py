import os
import pathlib
import json
from queue import Queue


class PerfLogger:
    def __init__(self):
        log_dir = os.path.join(
            pathlib.Path(__file__).parent.resolve(),
            'log',
        )
        log_inner_dir = os.path.join(
            log_dir,
            'perf',
        )
        self.log_file = os.path.join(
            log_inner_dir,
            'durations.json',
        )

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        if not os.path.exists(log_inner_dir):
            os.mkdir(log_inner_dir)

    def write_duration(self, key, duration):
        with open(self.log_file, 'r+') as f:
            try:
                data = json.load(f) or {}
            except json.JSONDecodeError:
                data = {}

            durations = data.get(key, [])
            durations.append(duration)
            data = {
                **data,
                str(key): duration,
            }

            json.dump(data, f, indent=4)


q = Queue()


def perf_logger_worker(observations_queue):
    perf_logger = PerfLogger()

    while True:
        (key, duration) = observations_queue.get()
        perf_logger.write_duration(key, duration)
        # observations_queue.task_done()

