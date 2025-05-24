# --- 📦 Стандартна бібліотека ---
import argparse
import csv
import os
import json
import random
from threading import Event

import numpy as np

# --- 📁 Внутрішні модулі ---
from config import (
    CACHE_CAPACITY, NUM_OBJECTS, NUM_REQUESTS, DELAY_T,
    CHECK_INTERVAL,
    LOGREG_MODEL_PATH,
    ALPHA, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    ETA_START, ETA_MIN, ETA_DECAY_K,
    STATS_FILE,
    PARAMS_PATH, params
)

from domain.object import ObjectData
from generator.object_generator import ObjectGenerator
from generator.request_generator import RequestGenerator

from cache.in_memory_cache import InMemoryCache
from cache.classics import LRUCache, LFUCache

from utils.persistent import (
    save_objects, load_objects,
    save_q_table, load_q_table
)
from utils.init_helpers import init_logreg
from utils.shared_index import SharedIndex

from agents.q_learning_agent import QLearningAgent
from agents.logreg_agent import LogRegAgent

from buffers.q_buffer import QBuffer
from buffers.logreg_buffer import LogRegBuffer

from updater.q_updater import QUpdater
from updater.logreg_updater import LogRegUpdater

parser = argparse.ArgumentParser()
parser.add_argument("--reset", type=int, default=0)
args = parser.parse_args()

if args.reset:
    from utils.reset import reset_all
    reset_all()

random.seed(42)
np.random.seed(42)
print("[Seed] ✅ Використовується фіксований random seed (режим стабільного тестування)")

# --- Створення початкового CSV і моделі, якщо треба ---
init_logreg()

# --- Ініціалізація ---
int_cache = InMemoryCache(max_size=CACHE_CAPACITY)
lru_cache = LRUCache(max_size=CACHE_CAPACITY)
lfu_cache = LFUCache(max_size=CACHE_CAPACITY)

q_buffer = QBuffer(delay_T=DELAY_T)
logreg_buffer = LogRegBuffer(delay_T=DELAY_T)
q_table = load_q_table()
reload_flag = Event()

q_agent = QLearningAgent(
    num_actions=2,
    alpha=ALPHA,
    gamma=GAMMA,
    epsilon_start=EPSILON_START,
    epsilon_min=EPSILON_MIN,
    epsilon_decay=EPSILON_DECAY,
    q_table=q_table,
    buffer=q_buffer
)

logreg_agent = LogRegAgent(
    model_path=LOGREG_MODEL_PATH,
    buffer=logreg_buffer,
    cache=int_cache,
    reload_flag=reload_flag
)

obj_gen = ObjectGenerator()
all_objects = load_objects()
if not all_objects:
    all_objects = {obj.id: obj for obj in obj_gen.generate_batch(NUM_OBJECTS)}
    save_objects(all_objects)

req_gen = RequestGenerator(object_ids=list(all_objects.keys()))
requests = req_gen.generate_requests(NUM_REQUESTS)

shared_index = SharedIndex(0)
q_updater = QUpdater(
    buffer=q_buffer,
    q_table=q_table,
    requests=requests,
    check_interval=CHECK_INTERVAL,
    shared_index=shared_index
)

logreg_updater = LogRegUpdater(
    buffer=logreg_buffer,
    requests=requests,
    reload_flag=reload_flag,
    check_interval=CHECK_INTERVAL,
    shared_index=shared_index
)

q_updater.start()
logreg_updater.start()

int_hits = 0
lru_hits = 0
lfu_hits = 0

interval = 100

# --- Основний цикл ---
for i in range(len(requests)):
    req = requests[i]
    object_id = req["object_id"]
    obj = all_objects[object_id]

    shared_index.set(i)

    # --- Підрахунок хітів ---
    if lru_cache.get(object_id) is not None:
        lru_hits += 1
    else:
        lru_cache.add(obj)
    if lfu_cache.get(object_id) is not None:
        lfu_hits += 1
    else:
        lfu_cache.add(obj)
    if int_cache.get(object_id) is None:
        action = q_agent.act(object_data=obj, current_index=i)
        if action == 1:
            if int_cache.is_full():
                to_evict = logreg_agent.act(current_index=i)
                if to_evict:
                    int_cache.delete(to_evict)
            int_cache.add(obj)
    else:
        int_hits += 1


print("[Main] ⏳ Очікування завершення роботи апдейтерів...")

q_updater.stop()
logreg_updater.stop()
q_updater.join()
logreg_updater.join()

# --- Збереження результатів ---
save_q_table(q_table)

with open(STATS_FILE, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([int_hits, lru_hits, lfu_hits])

params["EPSILON_START"] = max(EPSILON_MIN, EPSILON_START * (1 - EPSILON_DECAY))
params["ETA_START"] = max(ETA_MIN, ETA_START * (1 - ETA_DECAY_K))

with open(PARAMS_PATH, "w") as f:
    json.dump(params, f, indent=2)

print(f"[Main] 🔁 Оновлено ε={params['EPSILON_START']:.4f}, η={params['ETA_START']:.4f}")


# # -- Додаткова інформація про конфігурацію ---
# print("\n--- Конфігурація експерименту ---")
# print(f"Кількість унікальних обʼєктів:   {NUM_OBJECTS}")
# print(f"Обʼєм кешу:                      {CACHE_CAPACITY}")
# print(f"Загальна кількість запитів:      {NUM_REQUESTS}")
#
# # --- Підсумки ---
# print("\n--- Результати ---")
# print(f"Кеш-хіти (Intellectual):        {int_hits}")
# print(f"Кеш-хіти (LRU):                 {lru_hits}")
# print(f"Кеш-хіти (LFU):                 {lfu_hits}")
#
# # --- Порівняння у відсотках ---
# improvement_vs_lru = 100 * (int_hits - lru_hits) / lru_hits
# improvement_vs_lfu = 100 * (int_hits - lfu_hits) / lfu_hits
#
# print(f"\nПокращення порівняно з LRU:     {improvement_vs_lru:.2f}%")
# print(f"Покращення порівняно з LFU:     {improvement_vs_lfu:.2f}%")
#
# if improvement_vs_lru > 2. or improvement_vs_lru > 2.:
#     plot_cache_hits({
#         "Intellectual (QLearn + LogReg)": smart_curve,
#         "LRU": lru_curve,
#         "LFU": lfu_curve
#     }, interval)