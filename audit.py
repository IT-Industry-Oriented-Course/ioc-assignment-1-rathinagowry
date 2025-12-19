import json
from datetime import datetime
from typing import Any

def _json_safe(obj: Any):
    """
    Converts non-JSON-serializable objects (e.g., date)
    into safe representations.
    """
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    return str(obj)

def audit_log(event_type: str, payload: dict):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "payload": payload,
    }

    with open("audit.log", "a") as f:
        f.write(json.dumps(log_entry, default=_json_safe) + "\n")
