import threading
import time
from typing import List, Dict

from buffers.q_buffer import QBuffer
from buffers.q_table import QTable
from utils.features import simulate_new_state
from utils.history import was_requested_since


class QUpdater(threading.Thread):
    def __init__(
        self,
        buffer: QBuffer,
        q_table: QTable,
        requests: List[Dict],
        alpha: float,
        gamma: float,
        delay_t: int = 10,
        check_interval: float = 0.5
    ):
        super().__init__(daemon=True)
        self.buffer = buffer
        self.q_table = q_table
        self.requests = requests
        self.alpha = alpha
        self.gamma = gamma
        self.delay_t = delay_t
        self.check_interval = check_interval
        self.running = True
        self.current_index = 0  # Оновлюється ззовні через set_current_index()

    def run(self):
        while self.running:
            ready_items = self.buffer.get_ready_objects(self.delay_t)
            for state, action_str, obj_id, index_at in ready_items:
                new_state = simulate_new_state(state)

                # Оцінка винагороди на основі історії запитів
                was_req = was_requested_since(
                    requests=self.requests,
                    object_id=obj_id,
                    start_time=index_at,
                    end_time=self.current_index
                )
                reward = 1.0 if was_req else 0.0

                self.q_table.update(
                    state=state,
                    action=int(action_str),
                    reward=reward,
                    next_state=new_state,
                    alpha=self.alpha,
                    gamma=self.gamma
                )

            time.sleep(self.check_interval)

    def stop(self):
        """Зупиняє потік оновлення."""
        self.running = False

    def set_current_index(self, index: int):
        """Встановлює поточну мітку часу для оцінки запитів."""
        self.current_index = index