from threading import RLock


class Buffer:

    def __init__(self, max_size=None):
        self._lock = RLock()
        self._buffer = ''
        self._max_size = max_size

    def write(self, data):
        with self._lock:
            self._buffer = f'{self._buffer}\n{data}'[:self._max_size]

    def read(self, count):
        result = ''
        with self._lock:
            result, self._buffer = self._buffer[:count], self._buffer[count:]
        return result
