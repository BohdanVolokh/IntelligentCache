# utils/shared_index.py

import threading

class SharedIndex:
    def __init__(self, initial: int = 0):
        self._value = initial
        self._lock = threading.Lock()

    def set(self, new_value: int):
        with self._lock:
            self._value = new_value

    def get(self) -> int:
        with self._lock:
            return self._value