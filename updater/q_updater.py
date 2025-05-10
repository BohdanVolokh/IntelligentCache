import threading
import time
import random
from typing import Optional

from buffers.q_buffer import QBuffer
from db.in_memory_db import InMemoryStorage
from buffers.q_table import QTable

class QUpdater(threading.Thread):
    def __init__(
        self,
        buffer: QBuffer,
        q_table: QTable,
        storage: InMemoryStorage,
        alpha: float,
        gamma: float,
        delay_T: int = 10,
        check_interval: float = 0.5
    ):
        super().__init__(daemon=True)
        self.buffer = buffer
        self.q_table = q_table
        self.storage = storage
        self.alpha = alpha
        self.gamma = gamma
        self.delay_T = delay_T
        self.check_interval = check_interval
        self.running = True

    def run(self):
        while self.running:
            ready_items = self.buffer.get_ready_items(self.delay_T)
            for state, action_str, obj_id, index_at in ready_items:
                new_state = simulate_new_state(state)
                was_requested = self.storage.was_requested_since(obj_id, index_at)
                reward = 1.0 if was_requested else 0.0

                self.q_table.update(
                    state,
                    int(action_str),
                    reward,
                    new_state,
                    self.alpha,
                    self.gamma
                )

            time.sleep(self.check_interval)

    def stop(self):
        self.running = False


def simulate_new_state(old_state: list[float]) -> list[float]:
    """
    Імітація нового стану: кожна ознака трохи змінюється в межах [-0.05, +0.05],
    але залишається в діапазоні [0.0, 1.0].
    """
    return [
        max(0.0, min(1.0, x + random.uniform(-0.05, 0.05)))
        for x in old_state
    ]