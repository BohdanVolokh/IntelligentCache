from typing import List
import random
import math
#from features_extractor import extract_features  # припускаємо, що ця функція існує
from buffers.q_buffer import QBuffer
from buffers.q_table import QTable
from domain.object import ObjectData


class QAgent:
    def __init__(
        self,
        num_actions: int,
        alpha: float,
        gamma: float,
        epsilon_start: float,
        epsilon_min: float,
        epsilon_decay: float,
        q_table: QTable,
        buffer: QBuffer
    ):
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.q_table = q_table
        self.buffer = buffer

        self.step_count = 0

    def act(self, object_data : ObjectData, current_index: int) -> int:
        # Отримуємо ознаки об'єкта
        state = object_data.features

        # Оновлюємо epsilon за експоненційною формулою
        epsilon = max(
            self.epsilon_min,
            self.epsilon_start * math.exp(-self.epsilon_decay * self.step_count)
        )
        self.step_count += 1

        # Вибір дії за epsilon-жадібною стратегією
        if random.random() < epsilon:
            action = random.randint(0, self.num_actions - 1)  # дослідження
        else:
            action = self.q_table.argmax(state)  # експлуатація

        # Зберігаємо приклад для відкладеного оновлення
        self.buffer.add(state, str(action), object_data.id, current_index)

        return action
