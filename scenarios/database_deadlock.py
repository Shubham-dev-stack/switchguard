"""
Chaos Scenario: Connection Pool Exhaustion on Unhandled Transaction Exception
Service: billing-api (Tier-1)
Symptom: ConnectionPoolExhausted error after 10 failed checkout requests; service stops accepting queries.
Root Cause: Connection acquired before try block but not returned to pool in except block.
"""
from typing import List, Optional

class ConnectionPoolExhausted(Exception):
    pass

class MockDBConnection:
    def __init__(self, conn_id: int):
        self.conn_id = conn_id
        self.in_use = False

class MockConnectionPool:
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self._pool: List[MockDBConnection] = [MockDBConnection(i) for i in range(max_size)]

    def acquire(self) -> MockDBConnection:
        for conn in self._pool:
            if not conn.in_use:
                conn.in_use = True
                return conn
        raise ConnectionPoolExhausted("Database connection pool exhausted! No idle connections available.")

    def release(self, conn: MockDBConnection) -> None:
        conn.in_use = False

    @property
    def available_count(self) -> int:
        return sum(1 for c in self._pool if not c.in_use)


class BillingService:
    def __init__(self, pool: MockConnectionPool):
        self.pool = pool

    def process_charge(self, amount: float, buggy: bool = False) -> bool:
        conn = self.pool.acquire()
        if buggy:
            # Bug: if amount <= 0, raises ValueError before conn is released
            if amount <= 0:
                raise ValueError("Charge amount must be strictly positive")
            self.pool.release(conn)
            return True
        else:
            # Fixed: use try-finally to guarantee release back to pool
            try:
                if amount <= 0:
                    raise ValueError("Charge amount must be strictly positive")
                return True
            finally:
                self.pool.release(conn)
