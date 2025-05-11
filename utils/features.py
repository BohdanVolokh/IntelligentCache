import random

from config import FEATURE_KEYS, FEATURE_RANGES


def normalize_features(features: list[int]) -> list[float]:
    """
    Нормалізує кожну ознаку до діапазону [0.0, 1.0]
    """
    normalized = []
    for i, x in enumerate(features):
        key = FEATURE_KEYS[i]
        low, high = FEATURE_RANGES[key]
        norm = (x - low) / (high - low) if high > low else 0.0
        normalized.append(norm)
    return normalized


def simulate_new_state(old_state: list[float]) -> list[float]:
    """
    Імітація нового стану: кожна ознака трохи змінюється в межах [-0.05, +0.05],
    але залишається в діапазоні [0.0, 1.0].
    """
    return [
        max(0.0, min(1.0, x + random.uniform(-0.05, 0.05)))
        for x in old_state
    ]