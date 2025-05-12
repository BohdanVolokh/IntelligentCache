import time
import csv
import os
import threading
import subprocess
from typing import List, Dict
from threading import Event

from buffers.logreg_buffer import LogRegBuffer
from utils.history import was_requested_since
from config import (
    CHECK_INTERVAL,
    LOGREG_CSV_PATH,
    LOGREG_TRAIN_SCRIPT,
    LOGREG_RETRAIN_EVERY,
)


class LogRegUpdater(threading.Thread):
    def __init__(
        self,
        buffer: LogRegBuffer,
        requests: List[Dict],
        reload_flag: Event
    ):
        super().__init__(daemon=True)
        self.buffer = buffer
        self.requests = requests
        self.reload_flag = reload_flag
        self.csv_path = LOGREG_CSV_PATH
        self.current_index = 0
        self.index_lock = threading.Lock()

    def run(self):
        print("[LogRegUpdater] 🔄 Потік запущено", flush=True)
        while True:
            time.sleep(CHECK_INTERVAL)
            self.process_ready_objects()

    def set_current_index(self, index: int):
        with self.index_lock:
            self.current_index = index

    def process_ready_objects(self):
        with self.index_lock:
            index_copy = self.current_index

        ready = self.buffer.get_ready_objects(index_copy)
        if not ready:
            return

        new_rows = []
        for obj in ready:
            label = int(was_requested_since(
                obj.object_id,
                obj.timestamp,
                self.requests,
                index_copy
            ))
            row = obj.features + [label]
            new_rows.append(row)

        file_exists = os.path.isfile(self.csv_path)
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["x1", "x2", "x3", "x4", "x5", "x6", "label"])
            writer.writerows(new_rows)

        print(f"[LogRegUpdater] 📝 Додано {len(new_rows)} рядків до CSV", flush=True)
        self.trigger_training()

    def trigger_training(self):
        with open(self.csv_path, "r") as f:
            num_lines = sum(1 for _ in f) - 1  # -1 бо перший рядок — заголовок

        if num_lines > 0 and num_lines % LOGREG_RETRAIN_EVERY == 0:
            print(f"[LogRegUpdater] ✅ {num_lines} прикладів — запускаю навчання...", flush=True)
            subprocess.run(["python", LOGREG_TRAIN_SCRIPT])
            self.reload_flag.set()
            print("[LogRegUpdater] 🚩 Флаг оновлення встановлено (модель потребує reload)", flush=True)