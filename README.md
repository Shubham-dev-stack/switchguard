# 🛡️ SwitchGuard: Autonomous SRE Incident Response Engine

[![CI](https://github.com/Shubham-dev-stack/switchguard/actions/workflows/ci.yml/badge.svg)](https://github.com/Shubham-dev-stack/switchguard/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-brightgreen.svg)](https://www.python.org/)
[![Flip the Switch Hackathon](https://img.shields.io/badge/Flip%20the%20Switch-Submission-orange.svg)](https://github.com/sandbox-quantum/switch)
[![Tests: 23 Passed](https://img.shields.io/badge/Tests-23%20Passed%20(100%25)-success.svg)](tests/)

> **Flip the Switch Hackathon Submission**  
> *Powered by [Switch](https://github.com/sandbox-quantum/switch) (SandboxAQ / Alphabet), WeMakeDevs & DevTools Academy.*

---

## ⚡ The Problem: Incident Response at 2:00 AM

When a critical production outage (P0/P1) strikes:
- **Alert Fatigue & Confusion**: Monitoring systems (Sentry, Datadog, PagerDuty) flood engineers with hundreds of uncoordinated notifications.
- **Context Fragmentation**: Engineers juggle disjointed dashboards, stack traces, git blame logs, and frantic Discord/Slack threads.
- **Mean Time to Resolution (MTTR)** stretches into hours, causing direct revenue loss, customer churn, and burnt-out on-call teams.
- **Isolated AI Tools**: Modern AI coding agents (Claude Code, OpenCode, Codex) typically operate in private developer terminals, unable to participate in shared team chat rooms.

---

## 🚀 The Solution: SwitchGuard

**SwitchGuard** bridges autonomous AI coding agents directly into your team's incident war rooms (Discord, Slack, Teams) via **Switch**.

When an alert fires, SwitchGuard immediately spins up an **Autonomous Incident War Room**:
1. **Intelligent Triage & Blast Radius**: Evaluates Tier-1 vs Tier-2 service impact, calculates user disruption percentage, and projects estimated revenue loss.
2. **Real-time SLA Enforcement**: Automatically monitors enterprise MTTA (5 min) and MTTR (30 min) deadlines with countdown timers.
3. **Forensic Code Diagnostics**: Scrubs sensitive PII/tokens from stack traces, traces faulty execution frames to lines of code, and inspects recent deployment commits.
4. **Autonomous Remediation & Human-in-the-Loop Gate**: Synthesizes reproduction tests, drafts minimal code patches, runs automated regression verification, and requests human confirmation before production rollout.
5. **Audit-Ready Blameless Postmortems**: Generates structured postmortems including timeline tables, 5-Whys root cause analysis, and preventive action matrices.

---

## 🏗️ Architecture & Message Flow

```mermaid
flowchart TD
    A[🚨 Telemetry Alert\nSentry / Datadog / Webhook] -->|Discord Bridge| B[#incident-war-room]
    
    subgraph Switch & SwitchGuard Core Engine
        B --> C[🛡️ SwitchGuard Commander\nSeverity Triage & SLA Tracker]
        C -->|Triage & Blast Radius| D[🔍 Automated Diagnostics\nLog Parser, PII Redactor, Git Blame]
        D -->|Identified Defect| E[🛠️ Autonomous Agent / OpenCode\nReproduction Test & Patch Synthesis]
        E -->|Regression Runner| T[🧪 Pytest Test Suite\n100% Green Verification]
    end

    T -->|Post Diff & Status Board| F[👤 Human On-Call Engineer\n@Shubham]
    F -->|'Approve' in Discord| G[🚀 Production Restored & Postmortem Generated]
```

---

## 📊 Live Verification: The INC-502 Outage

During live testing in Discord `#incident-war-room`, SwitchGuard resolved a real P0 checkout outage in **2 minutes 51 seconds**:

| Metric | Traditional On-Call | SwitchGuard Autonomous Response | Improvement |
|---|---|---|---|
| **Mean Time to Acknowledge (MTTA)** | 12 - 25 minutes | **12 seconds** | **~100x Faster** |
| **Mean Time to Identify (MTTI)** | 30 - 45 minutes | **45 seconds** | **~50x Faster** |
| **Mean Time to Resolution (MTTR)** | 90 - 180 minutes | **2 minutes 51 seconds** | **~40x Faster** |
| **Human Fatigue** | High (Context Switching) | Low (Review & Approve Only) | **Zero Overhead** |

Read the full incident report: [docs/postmortems/INC-502-checkout-outage.md](docs/postmortems/INC-502-checkout-outage.md).

---

## 📂 Repository Structure

```
switchguard/
├── .github/workflows/ci.yml       # Multi-version GitHub Actions CI pipeline
├── core/                          # Core Incident Engine
│   ├── models.py                  # Severity, Incident, BlastRadius, Timeline
│   ├── classifier.py              # Tier-1/2 triage & financial risk estimator
│   ├── sla.py                     # SRE MTTA/MTTR deadline tracker
│   └── timeline.py                # Markdown status board renderer
├── diagnostics/                   # Autonomous Forensic Suite
│   ├── log_analyzer.py            # PII scrubber & stack trace parser
│   ├── healthcheck.py             # Synthetic service probe & latency benchmark
│   └── git_blame_inspector.py     # Deployment regression blame correlation
├── scenarios/                     # Multi-Service Chaos Reproductions
│   ├── jwt_expiry_regression.py   # Auth token expiration regression
│   ├── database_deadlock.py       # Connection pool exhaustion simulation
│   └── redis_cache_stampede.py    # Cache thundering herd mitigation
├── postmortem/                    # Audit & Compliance Engine
│   └── generator.py               # 5-Whys blameless postmortem generator
├── demo-service/                  # Production Checkout Microservice
│   ├── checkout.py                # Order calculation engine
│   └── test_checkout.py           # Unit & edge-case test suite
├── tests/                         # Pytest Suite (23 Tests, 100% Pass)
├── docs/postmortems/              # Generated Incident Postmortems
├── cli.py                         # SwitchGuard Operator CLI
├── switchguard.template.yaml      # Switch Declarative Agent Template
├── DEMO_SCRIPT.md                 # 2-3 minute video recording guide
├── pyproject.toml                 # Modern Python packaging specification
└── README.md
```

---

## 🛠️ CLI Quickstart

Install dependencies:
```bash
pip install -e .
```

### 1. Triage an Alert
```bash
python cli.py triage --service checkout --error ZeroDivisionError --error-rate 100
```
Output:
```
=== SwitchGuard Triage Result ===
Service:      checkout
Assigned:     P0
User Impact:  100.0%
Financial:    $450,000.00 USD
```

### 2. Run Synthetic Health Probe
```bash
python cli.py probe --service payment-gateway
```

### 3. Generate Blameless Postmortem
```bash
python cli.py postmortem --incident-id INC-502 --service checkout-service
```

### 4. Run Complete Test Suite
```bash
pytest tests/ -v
```

---

## 🔗 Upstream Contributions to Switch

As part of the **#FliptheSwitch** initiative, we have contributed core service connectors upstream to `sandbox-quantum/switch`:

1. **Supabase Connector**: [PR #1343](https://github.com/sandbox-quantum/switch/pull/1343)  
   *Adds Supabase database & auth management capabilities to Switch agents.*
2. **Sentry Connector**: [PR #1348](https://github.com/sandbox-quantum/switch/pull/1348)  
   *Enables real-time error telemetry ingestion and stack trace analysis directly in Switch rooms.*

---

## 📜 License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
