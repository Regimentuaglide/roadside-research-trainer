"""Windows named-mutex single-instance guard for Roadside Research Trainer."""
from __future__ import annotations

import sys
import atexit

_MUTEX_NAME = "Global\\RoadsideResearchTrainer.v0_9"
_handle = None


def acquire_instance_lock() -> bool:
    global _handle
    if sys.platform != "win32":
        return True
    try:
        import win32event
        import win32api
        import winerror
        _handle = win32event.CreateMutex(None, False, _MUTEX_NAME)
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            return False
        atexit.register(release_instance_lock)
        return True
    except Exception:
        return True


def release_instance_lock() -> None:
    global _handle
    if _handle is not None:
        try:
            import win32api
            win32api.CloseHandle(_handle)
        except Exception:
            pass
        _handle = None