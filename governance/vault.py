import time
import json
import hashlib
from typing import List, Dict, Any, Optional

class AuditChainTamperedError(Exception):
    pass

class AuditRecord:
    def __init__(self, index: int, incident_id: str, actor: str, action: str, details: str, prev_hash: str, timestamp: Optional[float] = None):
        self.index = index
        self.incident_id = incident_id
        self.actor = actor
        self.action = action
        self.details = details
        self.prev_hash = prev_hash
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = f"{self.index}|{self.incident_id}|{self.actor}|{self.action}|{self.details}|{self.prev_hash}|{self.timestamp}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "incident_id": self.incident_id,
            "actor": self.actor,
            "action": self.action,
            "details": self.details,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "hash": self.hash
        }

class AuditVault:
    """
    Immutable, cryptographic audit ledger for recording all autonomous incident actions and human approvals.
    Uses SHA-256 block chaining to guarantee tamper resistance.
    """

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self.chain: List[AuditRecord] = []
        self._init_genesis()

    def _init_genesis(self) -> None:
        genesis = AuditRecord(
            index=0,
            incident_id="SYSTEM",
            actor="switchguard-core",
            action="GENESIS",
            details="Audit Vault Initialized",
            prev_hash=self.GENESIS_HASH
        )
        self.chain.append(genesis)

    def record_event(self, incident_id: str, actor: str, action: str, details: str) -> AuditRecord:
        prev_hash = self.chain[-1].hash
        record = AuditRecord(
            index=len(self.chain),
            incident_id=incident_id,
            actor=actor,
            action=action,
            details=details,
            prev_hash=prev_hash
        )
        self.chain.append(record)
        return record

    def verify_integrity(self) -> bool:
        """
        Validates every record in the chain against its SHA-256 digest and previous hash.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            if current.prev_hash != prev.hash:
                raise AuditChainTamperedError(f"Block {i} prev_hash mismatch!")

            if current.hash != current.compute_hash():
                raise AuditChainTamperedError(f"Block {i} data corrupted or modified!")

        return True
