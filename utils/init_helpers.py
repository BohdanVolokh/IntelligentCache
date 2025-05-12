import os
import csv
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from config import LOGREG_CSV_PATH, LOGREG_MODEL_PATH

def init_logreg():
    # 1. Завжди створюємо новий CSV з 2 прикладами
    print("[Init] Створюю новий CSV для логістичної регресії...")
    os.makedirs(os.path.dirname(LOGREG_CSV_PATH), exist_ok=True)
    with open(LOGREG_CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x1", "x2", "x3", "x4", "x5", "x6", "label"])
        writer.writerow([5, 20, 1, 10, 1, 3, 0])
        writer.writerow([25, 90, 2, 1, 2, 6, 1])

    # 2. Модель створюємо лише, якщо її ще нема
    if not os.path.exists(LOGREG_MODEL_PATH):
        print("[Init] Створюю початкову модель логістичної регресії...")
        df = pd.read_csv(LOGREG_CSV_PATH)
        X = df.drop(columns=["label"]).values
        y = df["label"].values
        model = LogisticRegression(C=1.0, solver="lbfgs", max_iter=100)
        model.fit(X, y)
        joblib.dump(model, LOGREG_MODEL_PATH)
        print(f"[Init] Початкова модель збережена → {LOGREG_MODEL_PATH}")
    else:
        print("[Init] Модель вже існує — завантаження не потрібне.")