from threading import Lock
from collections import deque
from typing import Deque, List
from dataclasses import dataclass

@dataclass
class PendingLogRegObject:
    features: List[float]   # нормалізовані ознаки на момент видалення
    object_id: str          # id обʼєкта
    timestamp: int          # момент видалення з кешу

class LogRegBuffer:
    def __init__(self, delay_T: int):
        self.buffer: Deque[PendingLogRegObject] = deque()
        self.delay_T = delay_T
        self.lock = Lock()

    def add(self, features: List[float], object_id: str, current_index: int):
        with self.lock:
            self.buffer.append(PendingLogRegObject(features, object_id, current_index))

    def get_ready_objects(self, current_index: int) -> List[PendingLogRegObject]:
        ready = []
        with self.lock:
            while self.buffer and current_index - self.buffer[0].timestamp >= self.delay_T:
                ready.append(self.buffer.popleft())

        #print(f"[LogRegUpdater] 🔄 Buffer Len {len(ready)}, Current index: {current_index}", flush=True)
        return ready

    def size(self) -> int:
        with self.lock:
            return len(self.buffer)