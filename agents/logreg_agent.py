from typing import List, Optional
import numpy as np
import joblib

from domain.object import ObjectData
from buffers.logreg_buffer import LogRegBuffer
from cache.interface_cache import CacheInterface
from threading import Event


class LogRegAgent:
    def __init__(
        self,
        model_path: str,
        buffer: LogRegBuffer,
        cache: CacheInterface,
        reload_flag: Event
    ):
        self.model_path = model_path
        self.buffer = buffer
        self.cache = cache
        self.reload_flag = reload_flag
        self.model = joblib.load(model_path)

    def act(self, current_index: int) -> Optional[str]:
        #print(f"[LogRegAgent] 📝 {current_index}", flush=True)
        if self.reload_flag.is_set():
            self.reload_model()
            self.reload_flag.clear()

        if self.cache.is_empty():
            return None

        objects: List[ObjectData] = []
        for k in self.cache.keys():
            obj = self.cache.get(k)
            if obj is not None:
                objects.append(obj)

        if not objects:
            return None

        X = np.array([obj.features for obj in objects])
        probs = self.model.predict_proba(X)[:, 1]

        evict_index = int(np.argmin(probs))
        to_evict = objects[evict_index]

        self.buffer.add(to_evict.features, to_evict.id, current_index)
        return to_evict.id

    def reload_model(self):
        try:
            self.model = joblib.load(self.model_path)
            print(f"[LogRegAgent] 🔄 Модель оновлена з {self.model_path}")
        except Exception as e:
            print(f"[LogRegAgent] ❗️Помилка при оновленні моделі: {e}")