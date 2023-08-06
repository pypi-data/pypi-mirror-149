from logging.handlers import MemoryHandler


class CustomMemoryHandler(MemoryHandler):

    def emit(self, record):
        """
        Emit a record or append it to the buffer
        """
        if self.shouldFlush():
            self.flush()
        else:
            self.buffer.append(record)

    def shouldFlush(self):
        """
        Flush only when buffer is full
        """
        return len(self.buffer) >= self.capacity

    def flush(self) -> None:
        """
        Caches a number of logs in memory, and flushes all of them in one go.

        Example:
        capacity = 10
        memory_handler = CustomMemoryHandler(capacity,
                                             flushLevel=logging.WARNING,
                                             target=stream_handler)
        """
        self.acquire()
        try:
            if self.target:
                # Send to target all the logs
                for log in self.buffer:
                    self.target.handle(log)

                self.buffer.clear()

        finally:
            self.release()
