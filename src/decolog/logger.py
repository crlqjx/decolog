import os
import logging
import functools
import datetime as dt

from pathlib import Path
from reprlib import repr


class Logger:
    def __init__(
        self,
        app_name: str,
        dir_path: str | Path,
        log_level: int = logging.DEBUG,
        console_handler_level: int = logging.DEBUG,
        file_handler_level: int = logging.DEBUG,
    ):
        """Initialize the logger class

        Args:
            app_name (str): the application or process name
            dir_path (str): the directory path where the log will be saved
        log_level (int): level of the log according to the logging package (
                INFO, DEBUG, CRITICAL, ...)
        console_handler_level (int): level of the console handler logs
            according to the logging package
        file_handler_level (int): level of the file handler logs
            according to the logging package

        Returns:
            None
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

        # Create folder
        os.makedirs(dir_path, exist_ok=True)

        file_handler = logging.FileHandler(
            os.path.join(
                dir_path,
                f"{self.app_name.lower()}_{dt.date.today().strftime('%Y%m%d')}.log",
            )
        )

        file_handler.setLevel(file_handler_level)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

    def __call__(self, func=None, is_verbose=True):
        # func is None when decorator is called with a parameter (ex: @logger(is_verbose=True)
        if func is None:             

            # Return a partial function that will be called with the actual function
            return lambda f: self.__call__(f, is_verbose=is_verbose)
        
        @functools.wraps(func)
        def with_logging(*args, **kwargs):
            try:
                title = f"{func.__name__}("
                if args:
                    title = (
                        f"{title}*{repr(args)}, "
                        if is_verbose is False
                        else f"{title}*{args}, "
                    )
                if kwargs:
                    title = (
                        f"{title}**{repr(kwargs)}"
                        if is_verbose is False
                        else f"{title}**{kwargs}"
                    )

                title = f"{title})"
                self.log.debug(title)
                timer_start = dt.datetime.now()
                result = func(*args, **kwargs)
                timer_end = dt.datetime.now()
                timer = timer_end - timer_start
                log_message = (
                    f"executed {title} in {round(timer.total_seconds(), 4)} seconds"
                )
                self.log.debug(log_message)
                return result
            except Exception as e:
                self.log.critical(f"Exception {type(e)}: {str(e)}")
                raise e

        return with_logging
