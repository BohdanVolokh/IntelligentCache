import random
from typing import List
from domain.object import ObjectData


class ObjectGenerator:
    def __init__(self, num_types: int = 3, num_locations: int = 10):
        self.num_types = num_types
        self.num_locations = num_locations

    def generate_object(self, object_id: int) -> ObjectData:
        features = [
            random.randint(1, 30),                  # x1: унікальні користувачі
            random.randint(1, 100),                 # x2: загальна кількість запитів
            random.randint(0, self.num_types - 1),  # x3: тип обʼєкта
            random.randint(0, 96),                  # x4: години з моменту останнього запиту
            random.randint(0, 2),                   # x5: пріоритет
            random.randint(0, self.num_locations - 1)  # x6: локація
        ]
        return ObjectData(id=str(object_id), features=features)

    def generate_batch(self, count: int) -> List[ObjectData]:
        return [self.generate_object(i) for i in range(count)]