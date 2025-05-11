# config.py

# Генерація даних
NUM_OBJECTS = 100               # Скільки обʼєктів згенерувати
NUM_REQUESTS = 200              # Скільки запитів згенерувати

# Кеш
CACHE_CAPACITY = 20            # Максимальний розмір кешу

# Діапазони ознак
FEATURE_RANGES = {
    "x1": (1, 30),      # унікальні користувачі
    "x2": (1, 100),     # загальна кількість запитів
    "x3": (0, 2),       # тип обʼєкта
    "x4": (0, 96),      # години з моменту останнього запиту
    "x5": (0, 2),       # пріоритет
    "x6": (0, 9),       # локація
}

# Порядок ознак (важливо для відповідності індексам у списках)
FEATURE_KEYS = list(FEATURE_RANGES.keys())

# Параметри симуляції нового стану
STATE_SIMULATION_CONFIG = {
    "intensity": 5,              # Максимальне коливання числових ознак
    "categorical_threshold": 2,  # Ознаки з розкидом ≤ threshold вважаються категоріальними
}

# Q-learning
ALPHA = 0.5                    # Коефіцієнт навчання
GAMMA = 0.9                    # Коефіцієнт дисконтування
EPSILON_START = 0.8            # Початкове ε
EPSILON_MIN = 0.1              # Мінімальне ε
EPSILON_DECAY = 0.005          # Швидкість зменшення ε

# LogReg learning rate parameters
ETA_START = 0.1
ETA_MIN = 0.01
ETA_DECAY_K = 0.01

#LogReg
LOGREG_RETRAIN_EVERY = 100  # кожні N запитів агент оновлює модель
LOGREG_CSV_PATH = "train_logreg/train_logreg.csv"
LOGREG_TRAIN_SCRIPT = "train_logreg/train_logreg.py"
LOGREG_MODEL_PATH = "train_logreg/logreg_model.pkl"

# Відкладене оновлення
DELAY_T = 10                   # Через скільки кроків обʼєкт оновлюється
CHECK_INTERVAL = 0.5           # Частота перевірки готових прикладів