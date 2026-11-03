import time
from typing import Dict, Any, List, Optional, Callable

class DispatchFailureError(Exception):
    pass

class WebhookDispatcher:
    """
    Dispatches incident alerts to chat endpoints with retry policy and backoff.
    """

    def __init__(self, max_retries: int = 3, backoff_factor: float = 0.1):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.sent_history: List[Dict[str, Any]] = []

    def dispatch(
        self,
        endpoint_url: str,
        payload: Dict[str, Any],
        transport_fn: Optional[Callable[[str, Dict[str, Any]], bool]] = None
    ) -> bool:
        transport = transport_fn or (lambda url, data: True)
        attempts = 0

        while attempts < self.max_retries:
            attempts += 1
            try:
                success = transport(endpoint_url, payload)
                if success:
                    self.sent_history.append({
                        "url": endpoint_url,
                        "payload": payload,
                        "attempts": attempts,
                        "timestamp": time.time()
                    })
                    return True
            except Exception:
                pass
            
            # Exponential backoff
            time.sleep(self.backoff_factor * (2 ** (attempts - 1)))

        raise DispatchFailureError(f"Failed to dispatch payload to {endpoint_url} after {attempts} attempts")
