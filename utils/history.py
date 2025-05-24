from typing import List, Dict


def was_requested_since(object_id, start_time, requests, end_time) -> int:
    for req in requests:
        if start_time <= req["timestamp"] <= end_time and req["object_id"] == object_id:
            return 1
    return 0