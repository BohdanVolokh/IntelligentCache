from config import FEATURE_RANGES, FEATURE_KEYS
import random

def simulate_new_state(old_state: list[float]) -> list[float]:
    new_state = []
    for i, key in enumerate(FEATURE_KEYS):
        low, high = FEATURE_RANGES[key]
        range_span = high - low

        # Якщо ознака категоріальна (невелика кількість значень), залишаємо без змін
        if range_span <= 2:
            new_value = old_state[i]
        else:
            delta = random.uniform(-0.05 * range_span, 0.05 * range_span)
            new_value = max(low, min(high, old_state[i] + delta))

        new_state.append(round(new_value))  # або без round, якщо хочеш float
    return new_state