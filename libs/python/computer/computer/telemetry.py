"""Computer telemetry for tracking anonymous usage and feature usage."""

import platform
from core.telemetry import increment, is_telemetry_enabled, record_event

SYSTEM_INFO = {
    "os": platform.system().lower(),
    "os_version": platform.release(),
    "python_version": platform.python_version(),
}

__all__ = [
    "increment",
    "is_telemetry_enabled",
    "record_event",
    "record_computer_initialization",
]


def record_computer_initialization() -> None:
    if not is_telemetry_enabled():
        return
    record_event("computer_initialized", SYSTEM_INFO)