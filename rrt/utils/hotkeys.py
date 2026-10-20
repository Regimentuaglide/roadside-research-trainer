"""Normalize hotkey strings used by handlers and config."""
from __future__ import annotations

_ALIASES = {
    "esc": "escape",
    "del": "delete",
    "ins": "insert",
    "pgup": "page up",
    "pgdn": "page down",
}


def normalize_hotkey(key: str) -> str:
    k = key.strip().lower()
    return _ALIASES.get(k, k)