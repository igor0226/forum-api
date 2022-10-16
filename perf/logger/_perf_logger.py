import os
import pathlib
import json
from datetime import datetime
from config import app_config


class PerfLogger:
    def __init__(self):
        log_dir = app_config['logs_dir']
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
