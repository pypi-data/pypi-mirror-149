# Logger builder
Package meant to be a facade for native logging. It simplifies the creation of the logger and
using several handlers.

## Prerequisites
Python > 3.6

## Installation
The Package is available directly on the Python Package Index
```
pip install logger_builder

```

## Running
The use of the basic stream logger involves initialization of the formatter, stream handler factory,
logger builder, and running the create logger function.
```
from logger_builder import LoggerBuilder
from logger_builder.formatter import create_formatter
from logger_builder.handler.factory import StreamHandlerFactory

if __name__ == "__main__":
    formatter = create_formatter(simple_description=True)

    stream_handler_factory = StreamHandlerFactory(formatter)

    handler_factories = [stream_handler_factory]
    logger_builder = LoggerBuilder(handler_factories)
    logger = logger_builder.create_logger("example")

    logger.info(f"Log something")

```

Log to file , and buffering handler factories were implemented as well (FileHandlerFactory, and
MemoryHandlerFactory, respectively).
