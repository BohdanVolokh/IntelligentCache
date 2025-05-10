from typing import Protocol, runtime_checkable
from domain.object_data import ObjectData


@runtime_checkable
class AgentInterface(Protocol):
    def decide(self, obj: ObjectData, time_step: int) -> bool:
        """
        Приймає рішення: кешувати обʼєкт чи ні.
        """
        ...

    def observe(self, obj: ObjectData, action: bool, time_step: int) -> None:
        """
        Зберігає приклад для майбутнього оновлення моделі.
        """
        ...

    def update(self, current_time: int) -> None:
        """
        Проводить оновлення моделі (Q-таблиці або ваг) на основі накопичених прикладів.
        """
        ...