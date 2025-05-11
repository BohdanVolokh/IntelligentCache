import random
from typing import List
from domain.object import ObjectData
from config import FEATURE_KEYS, FEATURE_RANGES
from utils.features import normalize_features  # <- нове

class ObjectGenerator:
    def __init__(self):
        self.feature_keys = FEATURE_KEYS

    def generate_object(self, object_id: int) -> ObjectData:
        raw_features = [
            random.randint(*FEATURE_RANGES[key])
            for key in self.feature_keys
        ]
        features = normalize_features(raw_features)
        return ObjectData(id=str(object_id), features=features)

    def generate_batch(self, count: int) -> List[ObjectData]:
        return [self.generate_object(i) for i in range(count)]