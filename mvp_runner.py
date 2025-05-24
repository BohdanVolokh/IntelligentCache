import subprocess
import csv
import time
import os
import json
from config import STATS_FILE, NUM_RUNS, PARAMS_PATH
from utils.plotter import plot_cache_hits_per_session

# 🔁 Створити або очистити файл статистики
with open(STATS_FILE, "w", newline="") as f:
    pass  # порожній файл, готовий до запису

# 📌 Отримати повний шлях до main.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PATH = os.path.join(SCRIPT_DIR, "main.py")

print(f"📊 Запускаємо {NUM_RUNS} сесій кешування...\n")

for i in range(NUM_RUNS):
    print(f"🔁 Запуск {i+1}/{NUM_RUNS}")
    reset_flag = "1" if i == 0 else "0"
    #reset_flag = "0"

    if reset_flag == "1":
        default_params = {
            "ALPHA": 1,
            "GAMMA": 0.95,
            "EPSILON_START": 0.95,
            "EPSILON_MIN": 0.1,
            "EPSILON_DECAY": 0.01,
            "ETA_START": 0.9,
            "ETA_MIN": 0.1,
            "ETA_DECAY_K": 0.001
        }
        with open(PARAMS_PATH, "w") as f:
            json.dump(default_params, f, indent=2)

    result = subprocess.run(
        ["python", MAIN_PATH, "--reset", reset_flag],
        capture_output=True,
        text=True,
        cwd=SCRIPT_DIR
    )

    if result.returncode != 0:
        print(f"❌ Помилка при запуску main.py:\n{result.stderr}")
    else:
        print(f"✅ main.py завершився успішно")
        print(result.stdout.strip())  # або вимкни для тиші

    time.sleep(0.5)

# === 📊 Після всіх запусків: статистика та графік ===

int_total = 0
lru_total = 0
lfu_total = 0

int_list, lru_list, lfu_list = [], [], []

with open(STATS_FILE, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if not row:
            continue
        i, l, f_ = map(int, row)
        int_total += i
        lru_total += l
        lfu_total += f_
        int_list.append(i)
        lru_list.append(l)
        lfu_list.append(f_)

if not int_list:
    print("\n⚠️ Немає даних у run_stats.csv — жодна сесія не записала результат.")
    exit(0)

runs = len(int_list)
avg_int = int_total / runs
avg_lru = lru_total / runs
avg_lfu = lfu_total / runs

improvement_vs_lru = 100 * (avg_int - avg_lru) / avg_lru
improvement_vs_lfu = 100 * (avg_int - avg_lfu) / avg_lfu

print("\n=== 📊 ПІДСУМКИ ЗА ВСІ СЕСІЇ ===")
print(f"Середній кеш-хіт (Intellectual): {avg_int:.2f}")
print(f"Середній кеш-хіт (LRU):          {avg_lru:.2f}")
print(f"Середній кеш-хіт (LFU):          {avg_lfu:.2f}")
print(f"\nПокращення над LRU:              {improvement_vs_lru:.2f}%")
print(f"Покращення над LFU:              {improvement_vs_lfu:.2f}%")

plot_cache_hits_per_session(int_list, lru_list, lfu_list)