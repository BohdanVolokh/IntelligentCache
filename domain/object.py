from dataclasses import dataclass
from typing import List


@dataclass
class ObjectData:
    id: str
    features: List[float]