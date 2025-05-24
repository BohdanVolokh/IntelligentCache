import json
import os

# --- Шляхи та глобальні налаштування ---
PARAMS_PATH = "params.json"
STATS_FILE = "run_stats.csv"
NUM_RUNS = 30

# --- Генерація даних ---
NUM_OBJECTS = 100
NUM_REQUESTS = 100_00

# --- Кеш ---
CACHE_CAPACITY = 10

# --- Значення за замовчуванням ---
default_params = {
    "ALPHA": 1,
    "GAMMA": 0.95,
    "EPSILON_START": 0.9,
    "EPSILON_MIN": 0.1,
    "EPSILON_DECAY": 0.02,
    "ETA_START": 0.9,
    "ETA_MIN": 0.1,
    "ETA_DECAY_K": 0.02
}

# --- Спроба завантажити параметри з файлу ---
try:
    with open(PARAMS_PATH, "r") as f:
        params = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print(f"[Config] ⚠️ Не вдалося завантажити '{PARAMS_PATH}', використовую дефолтні параметри.")
    params = default_params.copy()

# --- Q-learning ---
ALPHA = params["ALPHA"]
GAMMA = params["GAMMA"]
EPSILON_START = params["EPSILON_START"]
EPSILON_MIN = params["EPSILON_MIN"]
EPSILON_DECAY = params["EPSILON_DECAY"]

# --- LogReg ---
ETA_START = params["ETA_START"]
ETA_MIN = params["ETA_MIN"]
ETA_DECAY_K = params["ETA_DECAY_K"]

# --- Діапазони ознак ---
FEATURE_RANGES = {
    "x1": (1, 30),    # унікальні користувачі
    "x2": (1, 100),   # кількість запитів
    "x3": (0, 2),     # тип обʼєкта
    "x4": (0, 96),    # години з останнього запиту
    "x5": (0, 2),     # пріоритет
    "x6": (0, 9),     # локація
}
FEATURE_KEYS = list(FEATURE_RANGES.keys())

# --- Симуляція нового стану ---
STATE_SIMULATION_CONFIG = {
    "intensity": 2,              # 🔽 Менше коливання — більш передбачуваний стан
    "categorical_threshold": 2,
}



# # --- Q-learning ---
# ALPHA = 1
# GAMMA = 0.95
# EPSILON_START = 0.95             # 🔼 Більше дослідження на початку
# EPSILON_MIN = 0.1
# EPSILON_DECAY = 0.01          # 🔽 Повільніше зменшення ε
#
# # --- LogReg навчання ---
# ETA_START = 0.9
# ETA_MIN = 0.1
# ETA_DECAY_K = 0.001

# --- LogReg контроль ---
LOGREG_RETRAIN_EVERY = 10
LOGREG_CSV_PATH = "train_logreg/train_logreg.csv"
LOGREG_TRAIN_SCRIPT = "train_logreg/train_logreg.py"
LOGREG_MODEL_PATH = "train_logreg/logreg_model.pkl"

# --- Відкладене оновлення ---
DELAY_T = 1000
CHECK_INTERVAL = 0.001