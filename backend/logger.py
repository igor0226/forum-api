from datetime import datetime
import os.path
import logging
import pathlib


class AppLogger:
    __logger: logging.Logger = None
    __dates_map = dict()

    def __init__(self):
        # ensure that log directory exists
        log_dir = os.path.join(
            pathlib.Path(__file__).parent.resolve(),
            'log',
        )
        log_inner_dir = os.path.join(
            log_dir,
            '1d',
        )

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        if not os.path.exists(log_inner_dir):
            os.mkdir(log_inner_dir)

    def info(self, message):
        logger = self._get_logger()
        logger.info(message)

    def error(self, message):
        logger = self._get_logger()
        logger.error(message)

    def _get_logger(self):
        curr_date = str(datetime.now().date())
    
        if not self.__dates_map.get(curr_date):
            self.__dates_map[curr_date] = True
            log_file_name = '{}.log'.format(curr_date)
            log_file_path = os.path.join(
                pathlib.Path(__file__).parent.resolve(),
                'log',
                '1d',
                log_file_name,
            )
    
            if not os.path.exists(log_file_path):
                # create file
                open(log_file_path, 'w')
    
            file_handler = logging.FileHandler(
                filename=log_file_path,
            )
            formatter = logging.Formatter(
                fmt='%(asctime)s %(name)s - %(levelname)s:%(message)s'
            )
            file_handler.setFormatter(formatter)

            self.__logger = logging.getLogger('date based logging')
            self.__logger.setLevel(logging.INFO)
            self.__logger.addHandler(file_handler)

        return self.__logger


app_logger = AppLogger()
