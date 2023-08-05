import logging
import sys

from .abstract import HandlerAbstract

class StreamHandler(HandlerAbstract):

    def __init__(self, formatter: logging.Formatter) -> None:
        self.formatter = formatter

    def add_handler(self, logger: logging.Logger) -> logging.Logger:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(self.formatter)
        logger.addHandler(stream_handler)

        return logger
