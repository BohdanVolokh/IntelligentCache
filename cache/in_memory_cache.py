from domain.object import ObjectData
from typing import Any, Optional, List
from cache.interface_cache import CacheInterface


class InMemoryCache(CacheInterface):
    def __init__(self, max_size: int):
        self.store: dict[str, ObjectData] = {}
        self.max_size = max_size

    def add(self, obj: ObjectData) -> None:
        self.store[obj.id] = obj

    def get(self, object_id: str) -> Optional[ObjectData]:
        return self.store.get(object_id)

    def delete(self, object_id: str) -> None:
        self.store.pop(object_id, None)

    def keys(self) -> List[str]:
        return list(self.store.keys())

    def __len__(self) -> int:
        return len(self.store)

    def is_empty(self) -> bool:
        return len(self.store) == 0

    def is_full(self) -> bool:
        return len(self.store) >= self.max_size