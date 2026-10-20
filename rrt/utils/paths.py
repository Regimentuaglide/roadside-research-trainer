"""Filesystem helpers for Roadside Research Trainer."""
from __future__ import annotations

import os
from pathlib import Path


def app_data_dir() -> Path:
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    p = Path(base) / "RRT"
    p.mkdir(parents=True, exist_ok=True)
    return p


def capture_dir() -> Path:
    p = app_data_dir() / "captures"
    p.mkdir(parents=True, exist_ok=True)
    return p


def session_dir() -> Path:
    p = app_data_dir() / "sessions"
    p.mkdir(parents=True, exist_ok=True)
    return p