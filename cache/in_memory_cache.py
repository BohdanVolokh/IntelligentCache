from typing import Any, Optional, List
from cache.interface_cache import CacheInterface


class InMemoryCache(CacheInterface):
    def __init__(self, max_size: int):
        self.store = {}
        self.max_size = max_size

    def get(self, key: Any) -> Optional[Any]:
        return self.store.get(key)

    def set(self, key: Any, value: Any) -> None:
        self.store[key] = value

    def delete(self, key: Any) -> None:
        if key in self.store:
            del self.store[key]

    def keys(self) -> List[Any]:
        return list(self.store.keys())

    def __len__(self) -> int:
        return len(self.store)