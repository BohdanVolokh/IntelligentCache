import threading
import time
from typing import List, Dict

from buffers.q_buffer import QBuffer
from buffers.q_table import QTable
from utils.shared_index import SharedIndex
from utils.features import simulate_new_state
from utils.history import was_requested_since

class QUpdater(threading.Thread):
    def __init__(
        self,
        buffer: QBuffer,
        q_table: QTable,
        requests: List[Dict],
        check_interval: float,
        shared_index: SharedIndex
    ):
        super().__init__(daemon=True)
        self.buffer = buffer
        self.q_table = q_table
        self.requests = requests
        self.check_interval = check_interval
        self.running = True
        self.shared_index = shared_index


    def run(self):
        print("[QUpdater] 🔄 Потік запущено", flush=True)
        while self.running:
            self.process_ready_objects()
            time.sleep(self.check_interval)

    def process_ready_objects(self):
        index_copy = self.shared_index.get()
        ready = self.buffer.get_ready_objects(index_copy)
        if not ready:
            #print("[QUpdater] None", flush=True)
            return

        for pending in ready:
            state = pending.state
            action = pending.action
            obj_id = pending.object_id
            index_at = pending.timestamp
            new_state = simulate_new_state(state)

            was_req = was_requested_since(
                requests=self.requests,
                object_id=obj_id,
                start_time=index_at,
                end_time=index_copy
            )

            reward = self.q_table.compute_reward(action, was_req)

            self.q_table.update(
                state=state,
                action=action,
                reward=reward,
                next_state=new_state
            )

    def stop(self):
        self.running = False