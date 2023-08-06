from abc import ABC, abstractmethod
from logging import DEBUG, Logger, Handler


class HandlerFactoryAbstract(ABC):

    @abstractmethod
    def create_handler(self,
                       logging_level: int = DEBUG
                       ) -> Handler:
        ...

    @abstractmethod
    def add_handler(self, logger: Logger, logging_level: int = DEBUG) -> Logger:
        ...
