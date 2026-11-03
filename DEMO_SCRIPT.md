# 🎬 SwitchGuard: 2-3 Minute Video Demo Script

This script is designed for your hackathon submission video. Follow these exact steps for a high-impact presentation that scores maximum points with the judges.

---

### ⏱️ Act 1: The Hook & The Problem (0:00 – 0:35)
* **What to show**: Your webcam / face or title slide, then switch to your Discord screen.
* **What to say**:
  > *"Hi everyone, I’m Shubham, and this is **SwitchGuard** — an autonomous incident response war room commander powered by Switch.*
  > *When a critical P0 outage strikes in production at 2:00 AM, on-call engineers are inundated with alert fatigue. Context is scattered across logs, git blame, and chaotic Slack and Discord threads. Mean Time to Resolution drags into hours, costing businesses thousands of dollars per minute of downtime.*
  > *While AI coding agents are powerful, they are currently trapped in isolated local terminals. We built SwitchGuard to bring multi-agent engineering squads directly into your team's Discord and Slack channels."*

---

### ⏱️ Act 2: Live War Room in Discord (0:35 – 2:00)
* **What to show**: Discord `#incident-war-room` channel.
* **Action**:
  1. Highlight your trigger message:
     ```text
     @switch-buddy-admin [ALERT P0] Production checkout service is failing with ZeroDivisionError on 100% discount promo orders! Please investigate checkout.py and propose a fix.
     ```
  2. Scroll to the bot's live execution and result:
     - Show the **15 tool calls** executed autonomously on the system.
     - Show the bot locating `demo-service/checkout.py`.
     - Show the bot reading the code, pinpointing line 24 (`savings_ratio = round(subtotal / net_total, 2)`).
     - Show the bot editing `checkout.py` to add zero-division protection.
     - Show the bot executing `pytest` in the background and verifying all 3 tests pass.
* **What to say**:
  > *"Watch what happens in our Discord war room. When our P0 alert arrived, our Switch agent didn't just generate a generic chat response. It autonomously searched the codebase, located the faulty checkout service, isolated the ZeroDivisionError on line 24, applied the code fix, and ran the test suite locally.*
  > *Within seconds, it reported back in Discord with the exact line number, root cause explanation, and confirmation that all unit tests are green."*

---

### ⏱️ Act 3: Human-in-the-Loop & Architecture (2:00 – 2:40)
* **What to show**: Switch Console (showing the `SwitchGuard` template) and architecture diagram from `README.md`.
* **What to say**:
  > *"Crucially, SwitchGuard enforces a strict Human-in-the-Loop safety gate. Agents never deploy untested changes to production. The squad presents the patch to the on-call engineer for explicit signoff before any merge.*
  > *Under the hood, SwitchGuard is built on declarative Switch YAML templates, leveraging Switch's Model Context Protocol (MCP) server, multi-agent targeted messaging, and collaboration bridges."*

---

### ⏱️ Act 4: Conclusion (2:40 – 3:00)
* **What to say**:
  > *"With SwitchGuard and Switch, we turn chaotic middle-of-the-night outages into structured, 2-minute autonomous resolutions while keeping human engineers firmly in control.*
  > *Thank you to SandboxAQ, WeMakeDevs, and DevTools Academy for hosting the Flip the Switch hackathon!"*
