"""Checks GitHub releases for a newer Roadside Research Trainer build."""
from __future__ import annotations

import json
import urllib.request

from rrt import __version__
from rrt.utils.logging_setup import get_logger

log = get_logger("updater")

_RELEASE_URL = "https://api.github.com/repos/roadside-research-trainer/rrt/releases/latest"


def check_for_updates(timeout: float = 5.0) -> str | None:
    try:
        req = urllib.request.Request(_RELEASE_URL, headers={"User-Agent": f"RRT/{__version__}"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
    except Exception as exc:
        log.debug("update check failed: %s", exc)
        return None
    latest = data.get("tag_name", "").lstrip("v")
    if latest and latest != __version__:
        return latest
    return None