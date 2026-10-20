# Contributing to Roadside Research Trainer

Thanks for your interest in improving Roadside Research Trainer (RRT). This project is an open-source field-research toolkit for roadside data collection, route annotation, and pattern analysis on Windows.

## Development Setup

1. Install Python 3.11+ (64-bit recommended).
2. `python -m venv .venv && .venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Launch the trainer: `python -m rrt.bootstrap`

## Project Layout

- `rrt/bootstrap/` — application entry, window bootstrap, single-instance lock
- `rrt/core/` — route engine, capture pipeline, session orchestrator
- `rrt/handlers/` — feature handlers (route, annotation, capture, overlay)
- `rrt/services/` — background services (telemetry, export, updater)
- `rrt/models/` — dataclasses for routes, waypoints, sessions
- `rrt/utils/` — helpers (paths, logging, screen math)
- `tests/` — unit tests (pytest)

## Coding Standards

- Python 3.11, type hints required on public functions.
- `ruff` for linting, `black` for formatting.
- Keep handlers stateless where possible; push state into `models/`.
- Any new hotkey must be registered in `rrt/utils/hotkeys.py`.

## Pull Requests

- One feature per PR. Include a brief test in `tests/`.
- Update `CHANGELOG` in the release branch only.
- Roadside Research Trainer is intended for **educational and personal field-research use only**. Do not submit PRs that target third-party services without permission.

## Reporting Bugs

Use the issue template. Include OS build, Python version, and the tail of `%APPDATA%/RRT/logs/session.log`.