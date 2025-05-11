from collections import OrderedDict, defaultdict
from typing import Optional, List
from domain.object import ObjectData
from cache.interface_cache import CacheInterface


class LRUCache(CacheInterface):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.store = OrderedDict()

    def add(self, obj: ObjectData):
        object_id = obj.id
        if object_id in self.store:
            return  # обʼєкт уже є в кеші
        if len(self.store) >= self.max_size:
            self.store.popitem(last=False)
        self.store[object_id] = obj

    def get(self, object_id: str) -> Optional[ObjectData]:
        if object_id in self.store:
            self.store.move_to_end(object_id)
            return self.store[object_id]
        return None

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


class LFUCache(CacheInterface):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.store = {}
        self.freq = defaultdict(int)
        self.insert_order = {}  # для розв'язання конфліктів
        self._time_counter = 0

    def add(self, obj: ObjectData):
        object_id = obj.id
        if object_id in self.store:
            return  # обʼєкт уже є в кеші
        if len(self.store) >= self.max_size:
            to_evict = min(
                self.freq.items(),
                key=lambda item: (item[1], self.insert_order.get(item[0], float("inf")))
            )[0]
            self.delete(to_evict)

        self.insert_order[object_id] = self._time_counter
        self._time_counter += 1
        self.store[object_id] = obj
        self.freq[object_id] = 1

    def get(self, object_id: str) -> Optional[ObjectData]:
        if object_id in self.store:
            self.freq[object_id] += 1
            return self.store[object_id]
        return None

    def delete(self, object_id: str) -> None:
        self.store.pop(object_id, None)
        self.freq.pop(object_id, None)
        self.insert_order.pop(object_id, None)

    def keys(self) -> List[str]:
        return list(self.store.keys())

    def __len__(self) -> int:
        return len(self.store)

    def is_empty(self) -> bool:
        return len(self.store) == 0

    def is_full(self) -> bool:
        return len(self.store) >= self.max_size
