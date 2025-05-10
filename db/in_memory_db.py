import random
from typing import Dict, Optional, List
from domain.object import ObjectData
from db.interface_db import BaseStorage


class InMemoryStorage(BaseStorage):
    def __init__(self):
        self.storage: Dict[str, ObjectData] = {}

    def add(self, obj: ObjectData) -> None:
        self.storage[obj.id] = obj

    def get(self, object_id: str) -> Optional[ObjectData]:
        return self.storage.get(object_id)

    def get_all_ids(self) -> List[str]:
        return list(self.storage.keys())

    def get_random(self) -> Optional[ObjectData]:
        if not self.storage:
            return None
        return random.choice(list(self.storage.values()))