from perf.logger._perf_logger import PerfLogger


def perf_logger_worker(observations_queue):
    perf_logger = PerfLogger()

    while True:
        (key, duration) = observations_queue.get()
        perf_logger.write_duration(key, duration)
