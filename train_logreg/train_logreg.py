import os
import sys
import math
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression

# --- Додаємо корінь проєкту до sys.path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import ETA_START, ETA_MIN, ETA_DECAY_K, LOGREG_CSV_PATH, LOGREG_MODEL_PATH

def adaptive_eta(t: int) -> float:
    return max(ETA_MIN, ETA_START * math.exp(-ETA_DECAY_K * t))

def train_logreg(csv_path: str = LOGREG_CSV_PATH, model_path: str = LOGREG_MODEL_PATH):
    df = pd.read_csv(csv_path)
    if df.empty:
        print("Немає даних для тренування.")
        return

    X = df.drop(columns=["label"]).values
    y = df["label"].values

    eta = adaptive_eta(len(df))
    C = 1.0 / eta

    model = LogisticRegression(C=C, solver="lbfgs", max_iter=100)
    model.fit(X, y)
    joblib.dump(model, model_path)

    print(f"Збережено модель у {model_path} (η_t = {eta:.5f})", flush=True)

if __name__ == "__main__":
    train_logreg()