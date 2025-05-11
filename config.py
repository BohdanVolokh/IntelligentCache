# config.py

# --- Генерація даних ---
NUM_OBJECTS = 5000               # Менше обʼєктів → більше шансів на повторення
NUM_REQUESTS = 10000               # Достатньо запитів для навчання

# --- Кеш ---
CACHE_CAPACITY = 100             # Зменшений розмір кешу, щоб eviction мав значення

# --- Діапазони ознак ---
FEATURE_RANGES = {
    "x1": (1, 30),      # унікальні користувачі
    "x2": (1, 100),     # загальна кількість запитів
    "x3": (0, 2),       # тип обʼєкта
    "x4": (0, 96),      # години з моменту останнього запиту
    "x5": (0, 2),       # пріоритет
    "x6": (0, 9),       # локація
}
FEATURE_KEYS = list(FEATURE_RANGES.keys())

# --- Симуляція нового стану ---
STATE_SIMULATION_CONFIG = {
    "intensity": 3,              # Менша флуктуація дає стабільніші нові стани
    "categorical_threshold": 2,
}

# --- Q-learning ---
ALPHA = 0.1                    # Трохи менше навчання за крок
GAMMA = 0.95                   # Довший горизонт оцінки винагород
EPSILON_START = 1.0            # Стартуємо з максимуму дослідження
EPSILON_MIN = 0.05             # Можна нижче, щоб краще експлуатувати
EPSILON_DECAY = 0.0031         # Повільніше зниження — довше дослідження

# --- LogReg навчання ---
ETA_START = 0.3                # Сильніший стартовий градієнт
ETA_MIN = 0.01
ETA_DECAY_K = 0.005            # Повільніше згасання — стабільне навчання

# --- LogReg контроль ---
LOGREG_RETRAIN_EVERY = 200     # Не надто часто, аби уникнути шуму
LOGREG_CSV_PATH = "train_logreg/train_logreg.csv"
LOGREG_TRAIN_SCRIPT = "train_logreg/train_logreg.py"
LOGREG_MODEL_PATH = "train_logreg/logreg_model.pkl"

# --- Відкладене оновлення ---
DELAY_T = 50                   # Швидше накопичення даних для навчання
CHECK_INTERVAL = 0.3           # Частіше перевіряємо буфер