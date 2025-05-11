import random
from typing import List
from domain.object import ObjectData
from utils.features import normalize_features


class ObjectGenerator:
    def __init__(self, num_types: int = 3, num_locations: int = 10):
        self.num_types = num_types
        self.num_locations = num_locations

    def generate_object(self, object_id: int) -> ObjectData:
        object_type = random.randint(0, self.num_types - 1)

        # Гарячі обʼєкти (тип 0)
        if object_type == 0:
            x1 = random.randint(20, 30)
            x2 = random.randint(60, 100)
            x4 = random.randint(0, 24)
            x5 = random.randint(1, 2)
        # Теплі обʼєкти (тип 1)
        elif object_type == 1:
            x1 = random.randint(10, 20)
            x2 = random.randint(30, 60)
            x4 = random.randint(24, 72)
            x5 = random.randint(1, 2)
        # Холодні обʼєкти (тип 2)
        else:
            x1 = random.randint(1, 10)
            x2 = random.randint(1, 30)
            x4 = random.randint(72, 96)
            x5 = random.randint(0, 1)

        features = [
            x1,                                # x1: унікальні користувачі
            x2,                                # x2: загальна кількість запитів
            object_type,                       # x3: тип обʼєкта
            x4,                                # x4: години з моменту останнього запиту
            x5,                                # x5: пріоритет
            random.randint(0, self.num_locations - 1)  # x6: локація
        ]

        return ObjectData(id=str(object_id), features=features)

    def generate_batch(self, count: int) -> List[ObjectData]:
        return [self.generate_object(i) for i in range(count)]