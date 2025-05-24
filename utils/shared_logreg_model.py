
import threading
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression


class SharedLogRegModel:
    def __init__(self, model_path: str = "logreg_model.pkl"):
        self.model_path = model_path
        self.lock = threading.Lock()
        self.model = LogisticRegression()
        self._initialized = False

        try:
            self.model = joblib.load(self.model_path)
            self._initialized = True
        except FileNotFoundError:
            pass

    def predict_proba(self, x: list[float]) -> float:
        with self.lock:
            if not self._initialized:
                return 0.0
            x_np = np.array(x).reshape(1, -1)
            return float(self.model.predict_proba(x_np)[0][1])

    def train(self, X: list[list[float]], y: list[int]):
        with self.lock:
            X_np = np.array(X)
            y_np = np.array(y)
            self.model.fit(X_np, y_np)
            self._initialized = True
            joblib.dump(self.model, self.model_path)

    def is_initialized(self) -> bool:
        with self.lock:
            return self._initialized