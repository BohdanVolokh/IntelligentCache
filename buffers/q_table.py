from typing import Dict, List
from threading import Lock

class QTable:
    def __init__(self, num_actions: int):
        self.q_values: Dict[str, Dict[int, float]] = {}
        self.num_actions = num_actions
        self.lock = Lock()

    def _serialize_state(self, state: List[float]) -> str:
        return ".".join(map(str, state))

    def init_state_if_needed(self, state: List[float]) -> None:
        state_key = self._serialize_state(state)
        with self.lock:
            if state_key not in self.q_values:
                self.q_values[state_key] = {action: 0.0 for action in range(self.num_actions)}

    def get(self, state: List[float], action: int) -> float:
        state_key = self._serialize_state(state)
        with self.lock:
            return self.q_values.get(state_key, {}).get(action, 0.0)

    def set(self, state: List[float], action: int, value: float) -> None:
        self.init_state_if_needed(state)
        state_key = self._serialize_state(state)
        with self.lock:
            self.q_values[state_key][action] = value

    def update(self, state: List[float], action: int, reward: float, next_state: List[float], alpha: float, gamma: float) -> None:
        self.init_state_if_needed(state)
        self.init_state_if_needed(next_state)
        state_key = self._serialize_state(state)
        next_key = self._serialize_state(next_state)

        with self.lock:
            max_next_q = max(self.q_values[next_key].values())
            old_value = self.q_values[state_key][action]
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * max_next_q)
            self.q_values[state_key][action] = new_value

    def argmax(self, state: List[float]) -> int:
        self.init_state_if_needed(state)
        state_key = self._serialize_state(state)
        with self.lock:
            return max(self.q_values[state_key], key=self.q_values[state_key].get)

    # --- Додано для підтримки серіалізації ---
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = Lock()