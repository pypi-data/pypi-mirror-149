from collections import defaultdict
from contextlib import contextmanager
from logging import DEBUG, INFO  # noqa: F401 # pylint: disable=W0611
from threading import current_thread

from logzero import loglevel as set_loglevel  # noqa: F401 # pylint: disable=W0611
from logzero import logger as log  # noqa: F401 # pylint: disable=W0611
from logzero import LogFormatter, formatter as set_formatter

DEFAULT_FMT = '%(color)s[%(asctime)s] [%(process)d] [%(levelname)s] [%(threadName)s]%(end_color)s %(message)s'
DEBUG_FMT = ('%(color)s[%(asctime)s] [%(process)d] [%(levelname)s] [%(threadName)s] [%(processName)s:%(module)s:'
             '%(funcName)s:%(lineno)d]%(end_color)s %(message)s')


class DefaultLogFormatter(LogFormatter):  # pragma: no cover  # this class is never used directly
    def __init__(self, formatters,
                 default_format=DEFAULT_FMT,
                 date_format='%Y-%m-%d %H:%M:%S %z'):
        self.formats = defaultdict(lambda: default_format)
        for key, value in formatters.items():
            self.formats[key] = value
        LogFormatter.__init__(self, fmt=default_format, datefmt=date_format)

    def format(self, record):
        self._fmt = self.formats[record.levelno]
        return LogFormatter.format(self, record)


@contextmanager
def thread_name(new_name: str):
    thread = current_thread()
    original_name = thread.name
    thread.name = new_name
    try:
        yield
    finally:
        thread.name = original_name


set_formatter(DefaultLogFormatter({DEBUG: DEBUG_FMT},
                                  default_format=DEFAULT_FMT))
