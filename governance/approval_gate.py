import time
from typing import Set, Optional, Dict, Any

class UnauthorizedApproverError(Exception):
    pass

class ApprovalTimeoutError(Exception):
    pass

class ApprovalGate:
    """
    Enforces Human-in-the-Loop policy gate before code modifications or deployments.
    Validates approver identity against authorized roster and checks timeout limits.
    """

    def __init__(self, authorized_approvers: Set[str], timeout_seconds: float = 900.0):
        self.authorized_approvers = {a.lower().strip() for a in authorized_approvers}
        self.timeout_seconds = timeout_seconds
        # Active requests: incident_id -> {"requested_at": timestamp, "patch_hash": str, "status": str}
        self._pending_requests: Dict[str, Dict[str, Any]] = {}

    def request_approval(self, incident_id: str, patch_hash: str) -> None:
        self._pending_requests[incident_id] = {
            "requested_at": time.time(),
            "patch_hash": patch_hash,
            "status": "PENDING"
        }

    def evaluate_approval(self, incident_id: str, approver: str, decision: str) -> bool:
        """
        Evaluates approval decision ('approve' or 'reject').
        Raises:
            UnauthorizedApproverError: if approver is not authorized.
            ApprovalTimeoutError: if approval was received after timeout limit.
        """
        req = self._pending_requests.get(incident_id)
        if not req:
            raise ValueError(f"No pending approval request found for incident {incident_id}")

        clean_approver = approver.lower().strip().lstrip("@")
        if clean_approver not in self.authorized_approvers:
            raise UnauthorizedApproverError(
                f"User '{approver}' is not authorized to sign off on production patches."
            )

        elapsed = time.time() - req["requested_at"]
        if elapsed > self.timeout_seconds:
            req["status"] = "EXPIRED"
            raise ApprovalTimeoutError(
                f"Approval request for {incident_id} timed out after {int(elapsed)}s."
            )

        clean_decision = decision.lower().strip()
        if clean_decision in ("approve", "approved", "yes"):
            req["status"] = "APPROVED"
            return True
        else:
            req["status"] = "REJECTED"
            return False
