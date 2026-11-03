import time
import hashlib
from typing import Dict, Any, Optional, Tuple
from core.models import Alert

class AlertDeduplicator:
    """
    Sliding-window alert deduplicator and alert-storm suppressor.
    Groups recurring alerts by signature to prevent notification storms in team chat.
    """

    def __init__(self, window_seconds: float = 300.0):
        self.window_seconds = window_seconds
        # Mapping: fingerprint -> {"first_seen": timestamp, "last_seen": timestamp, "count": count, "alert": Alert}
        self._cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def compute_fingerprint(cls, alert: Alert) -> str:
        raw_key = f"{alert.service.lower()}:{alert.error_type.lower()}:{alert.source.lower()}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:16]

    def process(self, alert: Alert) -> Tuple[bool, int]:
        """
        Processes an incoming alert.
        Returns:
            (is_new_incident, total_count)
            is_new_incident is True only if this alert has not been seen in the current window.
        """
        now = time.time()
        fp = self.compute_fingerprint(alert)
        entry = self._cache.get(fp)

        # Check if entry exists and is within window
        if entry and (now - entry["last_seen"]) <= self.window_seconds:
            entry["count"] += 1
            entry["last_seen"] = now
            return (False, entry["count"])

        # New incident or window expired
        self._cache[fp] = {
            "first_seen": now,
            "last_seen": now,
            "count": 1,
            "alert": alert
        }
        return (True, 1)

    def get_storm_stats(self) -> Dict[str, Any]:
        return {
            "tracked_fingerprints": len(self._cache),
            "total_suppressed_alerts": sum(e["count"] - 1 for e in self._cache.values())
        }
