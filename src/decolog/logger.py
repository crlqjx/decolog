import os
import logging
import functools
import datetime as dt


class Logger:
    def __init__(
        self,
        app_name: str,
        dir_path: str,
        log_level: int = logging.DEBUG,
        console_handler_level: int = logging.DEBUG,
        file_handler_level: int = logging.DEBUG,
    ):
        """
        Initialize the logger class
        :param str app_name: the application or process name
        :param str dir_path: the directory path where the log will be saved
        :param int log_level: level of the log according to the logging package (INFO, 
        DEBUG, CRITICAL, ...)
        :param int console_handler_level: level of the console handler logs 
        according to the logging package
        :param int file_handler_level: level of the file handler logs 
        according to the logging package
        :return: None
        """

        self.app_name = app_name
        self.log = logging.getLogger(app_name)
        self.log.setLevel(console_handler_level)

        formatter = logging.Formatter(
            fmt="%(asctime)s|%(name)s|%(levelname)s:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_handler_level)
        console_handler.setFormatter(formatter)
        self.log.addHandler(console_handler)

        file_handler = logging.FileHandler(
            os.path.join(
                dir_path, f'{self.app_name.lower()}_{dt.date.today().strftime("%Y%m%d")}.log'
            )
        )

        file_handler.setLevel(file_handler_level)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

    def __call__(self, func):
        @functools.wraps(func)
        def with_logging(*args, **kwargs):
            try:
                self.log.debug(f"{func.__name__} - {args}")
                timer_start = dt.datetime.now()
                result = func(*args, **kwargs)
                timer_end = dt.datetime.now()
                timer = timer_end - timer_start
                log_message = (
                    f"executed {func.__name__} in {round(timer.total_seconds(), 2)} "
                    f"seconds with following arguments : {args}"
                )
                self.log.debug(log_message)
                return result
            except Exception as e:
                self.log.critical(f"Exception {type(e)}: {str(e)}")
                raise e

            return with_logging
