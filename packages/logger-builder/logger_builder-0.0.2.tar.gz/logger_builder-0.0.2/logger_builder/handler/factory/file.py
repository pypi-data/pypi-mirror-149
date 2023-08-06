from datetime import datetime
from logging import DEBUG, Formatter, Logger, FileHandler as FileHandlerLogging
from typing import TYPE_CHECKING

from .abstract import HandlerFactoryAbstract

if TYPE_CHECKING:
    from pathlib import Path


class FileHandlerFactory(HandlerFactoryAbstract):

    def __init__(self,
                 log_file_path: 'Path',
                 log_file_name: str,
                 formatter: Formatter
                 ) -> None:
        self.log_file_path = log_file_path
        self.log_file_name = log_file_name
        self.formatter = formatter

    def create_handler(self, logging_level: int = DEBUG) -> FileHandlerLogging:
        file_name = f'{datetime.now().date()}_{self.log_file_name}.log'
        file_handler = FileHandlerLogging(self.log_file_path / file_name)

        file_handler.setLevel(logging_level)
        file_handler.setFormatter(self.formatter)

        return file_handler

    def add_handler(self, logger: Logger, logging_level: int = DEBUG) -> Logger:
        file_handler = self.create_handler(logging_level)

        logger.addHandler(file_handler)

        return logger
