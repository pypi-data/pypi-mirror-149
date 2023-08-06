from logging import DEBUG, Formatter, Logger, StreamHandler as StreamHandlerLogging
import sys

from .abstract import HandlerFactoryAbstract


class StreamHandlerFactory(HandlerFactoryAbstract):

    def __init__(self, formatter: Formatter) -> None:
        self.formatter = formatter

    def create_handler(self, logging_level: int = DEBUG) -> StreamHandlerLogging:
        stream_handler = StreamHandlerLogging(sys.stdout)

        stream_handler.setLevel(logging_level)
        stream_handler.setFormatter(self.formatter)
        return stream_handler

    def add_handler(self, logger: Logger, logging_level: int = DEBUG) -> Logger:
        stream_handler = self.create_handler(logging_level)
        logger.addHandler(stream_handler)

        return logger
