import os
import pickle
from typing import Dict
from domain.object import ObjectData
from buffers.q_table import QTable

PERSIST_PATH = "persistent"
OBJECTS_FILE = os.path.join(PERSIST_PATH, "objects.pkl")
QTABLE_FILE = os.path.join(PERSIST_PATH, "q_table.pkl")

def save_objects(objects: Dict[str, ObjectData]):
    os.makedirs(PERSIST_PATH, exist_ok=True)
    with open(OBJECTS_FILE, "wb") as f:
        pickle.dump(objects, f)
    print("[Persistent] ✅ Обʼєкти збережені.")

def load_objects() -> Dict[str, ObjectData]:
    if not os.path.exists(OBJECTS_FILE):
        return {}
    with open(OBJECTS_FILE, "rb") as f:
        return pickle.load(f)

def save_q_table(q_table: QTable):
    os.makedirs(PERSIST_PATH, exist_ok=True)
    with open(QTABLE_FILE, "wb") as f:
        pickle.dump(q_table.q_values, f)  # тільки q_values, не весь об'єкт
    print("[Persistent] ✅ Q-таблиця збережена.")

def load_q_table() -> QTable:
    if os.path.isfile(QTABLE_FILE) and os.path.getsize(QTABLE_FILE) > 0:
        with open(QTABLE_FILE, "rb") as f:
            q_values = pickle.load(f)
        table = QTable(num_actions=2)
        table.q_values = q_values
        print("[Persistent] ✅ Q-таблиця успішно завантажена.")
        return table
    else:
        print("[Persistent] ⚠️ Q-таблиця не знайдена або порожня — створюю нову.")
        return QTable(num_actions=2)