from datetime import datetime
import logging
from typing import TYPE_CHECKING

from .abstract import HandlerAbstract

if TYPE_CHECKING:
    from pathlib import Path

class FileHandler(HandlerAbstract):

    def __init__(self,
                 log_file_path: 'Path',
                 formatter: logging.Formatter
                 ) -> None:
        self.log_file_path = log_file_path
        self.formatter = formatter

    def add_handler(self, logger: logging.Logger) -> logging.Logger:
        file_name = f'{datetime.now().date()}_{logger.name}.log'
        file_handler = logging.FileHandler(self.log_file_path / file_name)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)

        logger.addHandler(file_handler)

        return logger
