from typing import Protocol, List, Optional
from domain.object import ObjectData


class BaseStorage(Protocol):
    def add(self, obj: ObjectData) -> None:
        """Додає об'єкт у сховище."""
        ...

    def get(self, object_id: str) -> Optional[ObjectData]:
        """Повертає об'єкт за його ID або None, якщо не знайдено."""
        ...

    def get_all_ids(self) -> List[str]:
        """Повертає список усіх ідентифікаторів об'єктів."""
        ...

    def get_random(self) -> Optional[ObjectData]:
        """Повертає випадковий об'єкт (наприклад, для аналізу кеш-хітів)."""
        ...