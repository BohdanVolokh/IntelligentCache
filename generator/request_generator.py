from typing import List, Dict
import random


class RequestGenerator:
    def __init__(self, object_ids: List[str]):
        self.object_ids = object_ids

    def generate_requests(self, count: int) -> List[Dict]:
        requests = []
        for i in range(count):
            obj_id = random.choice(self.object_ids)
            request = {
                "object_id": obj_id,
                "timestamp": i  # умовна мітка часу
            }
            requests.append(request)
        return requests