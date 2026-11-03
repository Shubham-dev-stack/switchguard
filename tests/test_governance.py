import pytest
import time
from governance.approval_gate import ApprovalGate, UnauthorizedApproverError, ApprovalTimeoutError
from governance.vault import AuditVault, AuditChainTamperedError

def test_approval_gate_authorized_approve():
    gate = ApprovalGate(authorized_approvers={"Shubham", "sre-lead"}, timeout_seconds=60.0)
    gate.request_approval("INC-100", patch_hash="sha256:abc123patch")

    # Authorized user approves
    approved = gate.evaluate_approval("INC-100", approver="@Shubham", decision="Approve")
    assert approved is True

def test_approval_gate_unauthorized_rejection():
    gate = ApprovalGate(authorized_approvers={"Shubham"}, timeout_seconds=60.0)
    gate.request_approval("INC-100", patch_hash="sha256:abc123patch")

    # Unauthorized user attempts approval
    with pytest.raises(UnauthorizedApproverError):
        gate.evaluate_approval("INC-100", approver="@malicious_user", decision="Approve")

def test_approval_gate_timeout():
    gate = ApprovalGate(authorized_approvers={"Shubham"}, timeout_seconds=0.01)
    gate.request_approval("INC-100", patch_hash="sha256:abc123patch")
    
    time.sleep(0.02)
    with pytest.raises(ApprovalTimeoutError):
        gate.evaluate_approval("INC-100", approver="@Shubham", decision="Approve")

def test_audit_vault_integrity():
    vault = AuditVault()
    assert len(vault.chain) == 1
    assert vault.chain[0].action == "GENESIS"

    vault.record_event("INC-502", "switchguard-sentinel", "ALERT", "Received 500 error spike")
    vault.record_event("INC-502", "Shubham", "APPROVAL_GRANTED", "Signed off on checkout patch")
    vault.record_event("INC-502", "switchguard-fixer", "DEPLOYED", "Hotfix verified")

    assert len(vault.chain) == 4
    assert vault.verify_integrity() is True

def test_audit_vault_tamper_detection():
    vault = AuditVault()
    vault.record_event("INC-502", "Shubham", "APPROVAL_GRANTED", "Signed off on checkout patch")
    
    # Simulate attacker tampering with block data
    vault.chain[1].details = "Tampered details injected"
    with pytest.raises(AuditChainTamperedError):
        vault.verify_integrity()
