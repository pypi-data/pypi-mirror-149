from abc import ABC, abstractmethod
from logging import Logger

class HandlerAbstract(ABC):

    @abstractmethod
    def add_handler(self, logger: Logger) -> Logger:
        ...
