"""Screen capture pipeline used to snapshot roadside scenes during research."""
from __future__ import annotations

import time
from pathlib import Path

from rrt.core.route_engine import RouteEngine
from rrt.utils.paths import capture_dir
from rrt.utils.logging_setup import get_logger

log = get_logger("capture")


class CapturePipeline:
    """Grabs frames from the primary monitor at a throttled rate and links them to waypoints."""

    def __init__(self, engine: RouteEngine, fps: float = 1.0) -> None:
        self.engine = engine
        self.fps = max(0.1, min(fps, 10.0))
        self._last_grab = 0.0
        self._frames: list[Path] = []

    def _grab(self) -> Path | None:
        try:
            import mss
            from PIL import Image
        except ImportError:
            log.warning("capture deps missing (mss/pillow); skipping frame")
            return None
        out_dir = capture_dir()
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / f"frame_{int(time.time() * 1000)}.png"
        with mss.mss() as sct:
            shot = sct.grab(sct.monitors[1])
            Image.frombytes("RGB", shot.size, shot.rgb).save(target)
        self._frames.append(target)
        return target

    def tick(self) -> Path | None:
        now = time.monotonic()
        if now - self._last_grab < 1.0 / self.fps:
            return None
        self._last_grab = now
        frame = self._grab()
        if frame and self.engine.route.waypoints:
            self.engine.route.waypoints[-1].frame_path = str(frame)
        return frame

    def frame_count(self) -> int:
        return len(self._frames)