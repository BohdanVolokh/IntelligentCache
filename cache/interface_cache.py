from typing import Protocol, Any, Optional, List, runtime_checkable


@runtime_checkable
class CacheInterface(Protocol):
    def get(self, key: Any) -> Optional[Any]:
        """Повертає об'єкт із кешу за ключем або None, якщо його немає"""
        ...

    def set(self, key: Any, value: Any) -> None:
        """Додає або оновлює об'єкт у кеші за ключем"""
        ...

    def delete(self, key: Any) -> None:
        """Видаляє об'єкт із кешу за ключем"""
        ...

    def keys(self) -> List[Any]:
        """Повертає список усіх ключів у кеші"""
        ...

    def __len__(self) -> int:
        """Повертає поточну кількість обʼєктів у кеші"""
        ...
