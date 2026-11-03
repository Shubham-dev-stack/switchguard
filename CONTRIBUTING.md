# 🤝 Contributing to SwitchGuard

Thank you for your interest in contributing to SwitchGuard! As part of the **#FliptheSwitch** open-source initiative, we welcome contributions from the community.

---

## 🛠️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shubham-dev-stack/switchguard.git
   cd switchguard
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   pip install pytest pytest-cov ruff
   ```

---

## 🧪 Running the Test Suite

We maintain a strict 100% test pass policy. Before opening a Pull Request, ensure all tests pass:

```bash
pytest tests/ -v --cov=core --cov=diagnostics --cov=ingestion --cov=adapters --cov=governance --cov=postmortem --cov=scenarios
```

---

## 📋 Coding Standards

- **Code Style**: Follow PEP 8 guidelines. Format code using `ruff format` and verify with `ruff check`.
- **Commit Messages**: Follow Conventional Commits convention:
  - `feat(...)`: New features or modules
  - `fix(...)`: Bug fixes
  - `test(...)`: Unit tests or chaos scenarios
  - `docs(...)`: Documentation updates
- **Human-in-the-Loop Safety**: Never bypass approval checks or authorization gates.
