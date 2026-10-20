"""Global hotkey registration for Roadside Research Trainer."""
from __future__ import annotations

from typing import Callable

from rrt.utils.logging_setup import get_logger

log = get_logger("hotkeys")


class HotkeyHandler:
    def __init__(self) -> None:
        self._bindings: dict[str, Callable[[], None]] = {}
        self._active = False

    def bind(self, key: str, callback: Callable[[], None]) -> None:
        self._bindings[key.upper()] = callback
        log.debug("bound %s -> %s", key, getattr(callback, "__qualname__", callback))

    def start(self) -> None:
        try:
            import keyboard
        except ImportError:
            log.warning("keyboard module unavailable; hotkeys disabled")
            return
        for key, cb in self._bindings.items():
            keyboard.add_hotkey(key.lower(), cb, suppress=False)
        self._active = True
        log.info("registered %d hotkeys", len(self._bindings))

    def stop(self) -> None:
        if not self._active:
            return
        import keyboard
        keyboard.unhook_all_hotkeys()
        self._active = False
        log.info("hotkeys unregistered")