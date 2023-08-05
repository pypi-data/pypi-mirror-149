from logging import Formatter

def create_basic_formatter() -> Formatter:
    logs_format = (
        '%(asctime)s.%(msecs).0f - %(levelname)s - PID:%(process)d '
        '{%(name)s.%(funcName)s:%(lineno)d} %(message)s'
        )
    formatter = Formatter(fmt=logs_format, datefmt="%Y-%m-%d %H:%M:%S")
    return formatter
