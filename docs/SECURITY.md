# 🔒 Security & Compliance Policy

The SwitchGuard team takes security, human safety, and data confidentiality seriously.

---

## 1. Human-in-the-Loop Safety Invariant

SwitchGuard is architected with a strict security principle:
> **Autonomous agents CANNOT apply code changes, deploy containers, or execute database migrations to production environments without explicit human confirmation.**

1. All proposed diffs are staged locally and verified with `pytest`.
2. A cryptographic hash (`sha256`) of the patch is generated.
3. The diff is posted into team chat with an approval request.
4. An authorized engineer from the permitted roster must sign off via chat command (`Approve`) or interactive button.
5. All approvals are permanently written to the immutable SHA-256 Audit Vault.

---

## 2. PII & Secret Redaction

SwitchGuard automatically scrubs the following sensitive data patterns before broadcasting to chat or writing to logs:
- API Bearer Tokens (`Bearer [REDACTED_TOKEN]`)
- User Passwords (`password: "[REDACTED_SECRET]"`)
- Credit Card Numbers (`[REDACTED_CARD_NUMBER]`)
- Personal Email Addresses (`[REDACTED_EMAIL]`)

---

## 3. Vulnerability Reporting

If you discover a security vulnerability in SwitchGuard, please report it via GitHub Security Advisories or contact the maintainer at `shubham@users.noreply.github.com`. We respond within 24 hours.
