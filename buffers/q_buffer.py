from threading import Lock
from collections import deque
from typing import Deque, List
from dataclasses import dataclass

@dataclass
class PendingQObject:
    state: List[float]                     # стан обʼєкта на момент дії
    action: int                      # виконана дія (кешувати чи ні)
    object_id: str                   # id обʼєкта
    timestamp: int                  # індекс/час, коли додано приклад

class QBuffer:
    def __init__(self, delay_T: int):
        self.buffer: Deque[PendingQObject] = deque()
        self.delay_T = delay_T
        self.lock = Lock()

    def add(self, state: List[float], action: int, object_id: str, current_index: int):
        with self.lock:
            self.buffer.append(PendingQObject(state, action, object_id, current_index))

    def get_ready_objects(self, current_index: int) -> List[PendingQObject]:
        ready = []
        with self.lock:
            while self.buffer and current_index - self.buffer[0].timestamp >= self.delay_T:
                ready.append(self.buffer.popleft())
        return ready

    def size(self) -> int:
        with self.lock:
            return len(self.buffer)