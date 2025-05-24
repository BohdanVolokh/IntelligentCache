import time
import csv
import os
import threading
import subprocess
from typing import List, Dict
from threading import Event

from buffers.logreg_buffer import LogRegBuffer
from utils.history import was_requested_since
from utils.shared_index import SharedIndex
from config import (
    LOGREG_CSV_PATH,
    LOGREG_TRAIN_SCRIPT,
    LOGREG_RETRAIN_EVERY, CHECK_INTERVAL,
)


class LogRegUpdater(threading.Thread):
    def __init__(
        self,
        buffer: LogRegBuffer,
        requests: List[Dict],
        reload_flag: Event,
        check_interval: float,
        shared_index: SharedIndex
    ):
        super().__init__(daemon=True)
        self.buffer = buffer
        self.requests = requests
        self.reload_flag = reload_flag
        self.csv_path = LOGREG_CSV_PATH
        self.shared_index = shared_index
        self.check_interval = check_interval
        self.running = True
        self.last_trained_line_count = 0

    def run(self):
        print("[LogRegUpdater] 🔄 Потік запущено", flush=True)
        while self.running:
            self.process_ready_objects()
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False  # метод зупинки

    def process_ready_objects(self):
        index_copy = self.shared_index.get()
        ready = self.buffer.get_ready_objects(index_copy)
        if not ready:
            #print(f"[LogRegUpdater] 🔄 None {index_copy}", flush=True)
            return

        new_rows = []
        for obj in ready:
            label = was_requested_since(
                obj.object_id,
                obj.timestamp,
                self.requests,
                index_copy
            )
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
            num_lines = sum(1 for _ in f) - 1

        new_examples = num_lines - self.last_trained_line_count

        if new_examples >= LOGREG_RETRAIN_EVERY:
            print(f"[LogRegUpdater] ✅ {new_examples} прикладів — запускаю навчання...", flush=True)
            subprocess.run(["python", LOGREG_TRAIN_SCRIPT])
            self.reload_flag.set()
            self.last_trained_line_count = num_lines
            print("[LogRegUpdater] 🚩 Флаг оновлення встановлено (модель потребує reload)", flush=True)