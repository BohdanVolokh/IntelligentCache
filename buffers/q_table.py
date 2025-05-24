from typing import Dict, List
from threading import Lock

from config import (
    ALPHA, GAMMA
)

class QTable:
    def __init__(self, num_actions: int):
        self.q_values: Dict[str, Dict[int, float]] = {}
        self.num_actions = num_actions
        self.alpha = ALPHA
        self.gamma = GAMMA
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

    def update(self, state: List[float], action: int, reward: float, next_state: List[float]) -> None:
        self.init_state_if_needed(state)
        self.init_state_if_needed(next_state)
        state_key = self._serialize_state(state)
        next_key = self._serialize_state(next_state)

        with self.lock:
            # max_next_q = max(self.q_values[next_key].values())
            # old_value = self.q_values[state_key][action]
            # new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * max_next_q)
            old_value = self.q_values[state_key][action]
            new_value = (1 - self.alpha) * old_value + self.alpha * reward
            self.q_values[state_key][action] = new_value

    def argmax(self, state: List[float]) -> int:
        self.init_state_if_needed(state)
        state_key = self._serialize_state(state)
        with self.lock:
            q_values = self.q_values[state_key]
            #print(f"[QTable] Q-values: {q_values} for state {state}")
            return max(q_values, key=q_values.get)

    def compute_reward(self, action: int, was_requested: bool) -> float:
        """
        Обчислює винагороду для агента Q-learning.

        :param action: 1 — обʼєкт був закешований, 0 — обʼєкт не був закешований
        :param was_requested: чи був запит на обʼєкт після моменту прийняття рішення
        :return: числова винагорода
        """
        in_cache = action == 1

        if in_cache and was_requested:
            return 1.0  # (1) Кешував і обʼєкт повторно використано
        elif in_cache and not was_requested:
            return 0.0  # (2) Кешував, але обʼєкт не знадобився
        elif not in_cache and was_requested:
            return -1.0  # (4) Не кешував, але обʼєкт запитали
        else:
            return 0.0  # (3) Не кешував і обʼєкт не був потрібен

    # --- Додано для підтримки серіалізації ---
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = Lock()