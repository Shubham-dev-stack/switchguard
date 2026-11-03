# 🏛️ SwitchGuard Architecture & Internal Specification

SwitchGuard is an autonomous Site Reliability Engineering (SRE) incident response engine engineered to operate seamlessly over [Switch](https://github.com/sandbox-quantum/switch) (SandboxAQ / Alphabet).

---

## 1. High-Level System Architecture

SwitchGuard bridges telemetry systems (Sentry, Datadog, Prometheus) with team communication war rooms (Discord, Slack, Teams) and host-level coding agents (OpenCode, Claude Code):

```
+-------------------------------------------------------------------------+
|                        Ingestion & Telemetry                            |
|    [ Sentry Webhooks ]    [ Datadog Alerts ]    [ Prometheus Alerts ]   |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        SwitchGuard Core Engine                          |
|  - Ingestion Normalizer & Deduplicator (Sliding-Window Suppressor)      |
|  - Severity Classifier & Financial Blast Radius Estimator               |
|  - SRE SLA Tracker (MTTA < 5m, MTTR < 30m Real-time Deadlines)          |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                   Switch PostgreSQL Message Bus                         |
|     (LISTEN / pg_notify pubsub across Collaboration & Agent Bridges)    |
+--------------------+-------------------------------+--------------------+
                     |                               |
                     v                               v
+-----------------------------+     +-------------------------------------+
|    Collaboration Bridge     |     |       Switch Agent Controller       |
|  - Discord Embeds / Buttons |     |  - Host Sandbox Execution Daemon    |
|  - Slack Block Kit Actions  |     |  - OpenCode / FreeLLM / Claude Code |
|  - Interactive Status Board |     |  - Git Blame & Test Runner          |
+--------------+--------------+     +------------------+------------------+
               |                                       |
               +-------------------+-------------------+
                                   |
                                   v
+-------------------------------------------------------------------------+
|                   Human-In-The-Loop Governance Gate                     |
|  - Authorized Operator Signature Verification                           |
|  - SHA-256 Cryptographic Tamper-Evident Audit Vault                     |
+-------------------------------------------------------------------------+
```

---

## 2. Switch Core Integration Model

Switch operates an event-driven architecture powered by PostgreSQL:
1. **Templates (`templates` table)**: The `switchguard.template.yaml` defines the declarative persona, allowed shell capabilities, and room orchestration parameters.
2. **Postgres Message Bus**: Inter-agent communication is conducted over PostgreSQL notification channels. When an incident is triggered, SwitchGuard creates a dedicated war room thread.
3. **Agent Controller**: Switch's daemon manages tool execution (`run_command`, `read_file`, `edit_file`). The agent runs within the host environment, allowing it to execute tests (`pytest`), read source code, and stage verified git diffs.

---

## 3. Incident State Machine

Every incident progresses through a strict, deterministic state machine:

```
[ TRIGGERED ]
      |
      v  (Sentry / Webhook ingested, deduplicated)
[ ACKNOWLEDGED ]
      |
      v  (Commander opens War Room thread, assigns severity & blast radius)
[ INVESTIGATING ]
      |
      v  (Investigator runs stack trace scrubber & git blame correlation)
[ ROOT_CAUSE_IDENTIFIED ]
      |
      v  (Faulty line & function isolated in repository)
[ PATCHING ]
      |
      v  (Fixer synthesizes reproduction test & drafts code patch)
[ AWAITING_APPROVAL ]  <--- HUMAN-IN-THE-LOOP SAFETY GATE
      |
      +---> [ APPROVED ] ---> [ RESOLVED ] ---> [ POSTMORTEM_GENERATED ]
      |
      +---> [ REJECTED ] ---> [ ESCALATED_TO_HUMAN ]
```

---

## 4. Security & Compliance Guarantee

- **Zero Unchecked Deployments**: Autonomous agents are strictly prohibited from pushing code or merging PRs without an explicit `Approve` confirmation from an authorized engineer in chat.
- **PII & Secret Redaction**: All raw log payloads and stack traces pass through regex redaction masks that scrub Bearer tokens, passwords, credit card numbers, and emails before chat broadcast.
- **Cryptographic Audit Vault**: Every action taken by both human operators and autonomous agents is recorded into an append-only ledger secured by SHA-256 block chaining.
