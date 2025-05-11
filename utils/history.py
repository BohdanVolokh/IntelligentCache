from typing import List, Dict


def was_requested_since(object_id, start_time, requests, end_time):
    for req in requests:
        if not isinstance(req, dict):
            continue  # або raise Exception
        if start_time <= req["timestamp"] <= end_time and req["object_id"] == object_id:
            return True
    return False