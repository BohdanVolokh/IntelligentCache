from threading import Event
from config import (
    CACHE_CAPACITY, NUM_OBJECTS, NUM_REQUESTS, DELAY_T,
    LOGREG_MODEL_PATH
)
from domain.object import ObjectData
from generator.object_generator import ObjectGenerator
from generator.request_generator import RequestGenerator

from cache.in_memory_cache import InMemoryCache
from cache.classics import LRUCache
from cache.classics import LFUCache
from utils.plotter import plot_cache_hits

from agents.q_learning_agent import QLearningAgent
from agents.logreg_agent import LogRegAgent
from buffers.q_buffer import QBuffer
from buffers.logreg_buffer import LogRegBuffer
from updater.logreg_updater import LogRegUpdater
from updater.q_updater import QUpdater

# --- Ініціалізація ---
cache = InMemoryCache(max_size=CACHE_CAPACITY)
lru_cache = LRUCache(max_size=CACHE_CAPACITY)
lfu_cache = LFUCache(max_size=CACHE_CAPACITY)

q_buffer = QBuffer(delay_T=DELAY_T)
logreg_buffer = LogRegBuffer(delay_T=DELAY_T)

reload_flag = Event()

q_agent = QLearningAgent(buffer=q_buffer)
logreg_agent = LogRegAgent(
    model_path=LOGREG_MODEL_PATH,
    buffer=logreg_buffer,
    cache=cache,
    reload_flag=reload_flag
)

obj_gen = ObjectGenerator()
all_objects = {obj.id: obj for obj in obj_gen.generate_batch(NUM_OBJECTS)}

req_gen = RequestGenerator(object_ids=list(all_objects.keys()))
requests = req_gen.generate_requests(NUM_REQUESTS)

q_updater = QUpdater(buffer=q_buffer, requests=requests)
logreg_updater = LogRegUpdater(buffer=logreg_buffer, requests=requests, reload_flag=reload_flag)

q_updater.start()
logreg_updater.start()

int_hits = 0
lru_hits = 0
lfu_hits = 0

smart_curve, lru_curve, lfu_curve = [], [], []
interval = 100

# --- Основний цикл ---
for i in range(len(requests)):
    req = requests[i]

    object_id = req["object_id"]
    obj = all_objects[object_id]

    in_cache = cache.get(object_id) is not None

    # --- Підрахунок хітів ---
    if in_cache:
        int_hits += 1
    if lru_cache.get(object_id) is not None:
        lru_hits += 1
    else:
        lru_cache.add(obj)
    if lfu_cache.get(object_id) is not None:
        lfu_hits += 1
    else:
        lfu_cache.add(obj)

    if not in_cache:
        # --- Q-Learning агент: обрати дію ---
        action = q_agent.act(object_data=obj, current_index=i)
        if action == 1:
            if cache.is_full():
                to_evict = logreg_agent.act(current_index=i)
                if to_evict:
                    cache.delete(to_evict)
            cache.set(object_id, obj)

    # --- Оновлення індексу апдейтерів ---
    logreg_updater.set_current_index(i)
    q_updater.set_current_index(i)

    # --- Збір статистики ---
    if (i + 1) % interval == 0:
        smart_curve.append(int_hits / (i + 1))
        lru_curve.append(lru_hits / (i + 1))
        lfu_curve.append(lfu_hits / (i + 1))

# --- Підсумки ---
print("\n--- Результати ---")
print(f"Загальна кількість запитів:     {NUM_REQUESTS}")
print(f"Кеш-хіти (Intellectual):    {int_hits}")
print(f"Кеш-хіти (LRU):                 {lru_hits}")
print(f"Кеш-хіти (LFU):                 {lfu_hits}")

plot_cache_hits({
    "Intellectual (QLearn + LogReg)": smart_curve,
    "LRU": lru_curve,
    "LFU": lfu_curve
})