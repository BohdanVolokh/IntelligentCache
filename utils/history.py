from typing import List, Dict


def was_requested_since(requests: List[Dict], object_id: str, start_time: int, end_time: int) -> bool:
    """
    Перевіряє, чи був запит на object_id у проміжку [start_time, end_time).
    """
    for req in requests:
        if start_time <= req["timestamp"] <= end_time and req["object_id"] == object_id:
            return True
    return False