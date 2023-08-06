from abc import ABC, abstractmethod
from logging import Logger, DEBUG, getLogger
from typing import Sequence

from .handler.factory import HandlerFactoryAbstract


class LoggerBuilderAbstract(ABC):
    def __init__(self, handler_factories: Sequence[HandlerFactoryAbstract]) -> None:
        self._handler_factories = handler_factories

    def reset(self) -> None:
        self._handler_factories = []

    @abstractmethod
    def create_logger(self, logger_name: str, logging_level: int = DEBUG) -> Logger:
        """Method implemented in concrete class returning a logger"""


class LoggerBuilder(LoggerBuilderAbstract):
    def create_logger(self, logger_name: str, logging_level: int = DEBUG) -> Logger:
        logger = getLogger(logger_name)
        logger.setLevel(logging_level)

        for handler in self._handler_factories:
            logger = handler.add_handler(logger)

        return logger
