from typing import List, Dict
import random


class RequestGenerator:
    def __init__(self, object_ids: List[str]):
        self.object_ids = object_ids
        self.requests: List[Dict] = []  # Зберігає історію всіх запитів

    def generate_requests(self, count: int) -> List[Dict]:
        requests = []
        for i in range(count):
            obj_id = random.choice(self.object_ids)
            request = {
                "object_id": obj_id,
                "timestamp": i  # умовна мітка часу (можна замінити на len(self.requests) + i)
            }
            requests.append(request)
        self.requests.extend(requests)
        return requests

    def get_requests(self) -> List[Dict]:
        return self.requests