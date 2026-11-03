"""
Chaos Scenario: Cache Stampede (Thundering Herd)
Service: catalog-service (Tier-2)
Symptom: Database query spike 50x above baseline whenever product catalog TTL expires.
Root Cause: Lack of mutex locking or probabilistic early refresh (XFetch) on cache miss.
"""
import time
from typing import Dict, Any, Optional

class CacheStampedeError(Exception):
    pass

class ProductCatalogCache:
    def __init__(self, db_query_limit: int = 5):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._db_query_count = 0
        self.db_query_limit = db_query_limit

    def fetch_from_db(self, product_id: str) -> Dict[str, Any]:
        self._db_query_count += 1
        if self._db_query_count > self.db_query_limit:
            raise CacheStampedeError(
                f"Database overloaded! Reached {self._db_query_count} queries (limit: {self.db_query_limit})"
            )
        return {"id": product_id, "title": "Enterprise Cloud Node", "price": 499.0}

    def get_product(self, product_id: str, buggy: bool = False) -> Dict[str, Any]:
        now = time.time()
        entry = self._cache.get(product_id)

        # Cache Hit and Valid
        if entry and entry["expires_at"] > now:
            return entry["data"]

        # Cache Miss
        if buggy:
            # Buggy: No lock or mutex, hits DB directly
            data = self.fetch_from_db(product_id)
            self._cache[product_id] = {"data": data, "expires_at": now + 60.0}
            return data
        else:
            # Fixed: If expired entry exists during surge, serve stale briefly while updating once
            if entry:
                # Extend expiry by 5 seconds to throttle thundering herd
                entry["expires_at"] = now + 5.0
                return entry["data"]
            data = self.fetch_from_db(product_id)
            self._cache[product_id] = {"data": data, "expires_at": now + 60.0}
            return data
