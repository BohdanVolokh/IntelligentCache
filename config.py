# --- Генерація даних ---
NUM_OBJECTS = 50
NUM_REQUESTS = 100_000

# --- Кеш ---
CACHE_CAPACITY = 10

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

# --- Q-learning ---
ALPHA = 0.2
GAMMA = 0.95
EPSILON_START = 0.7             # 🔼 Більше дослідження на початку
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.0025          # 🔽 Повільніше зменшення ε

# --- LogReg навчання ---
ETA_START = 0.3
ETA_MIN = 0.01
ETA_DECAY_K = 0.005

# --- LogReg контроль ---
LOGREG_RETRAIN_EVERY = 100
LOGREG_CSV_PATH = "train_logreg/train_logreg.csv"
LOGREG_TRAIN_SCRIPT = "train_logreg/train_logreg.py"
LOGREG_MODEL_PATH = "train_logreg/logreg_model.pkl"

# --- Відкладене оновлення ---
DELAY_T = 300
CHECK_INTERVAL = 0.1