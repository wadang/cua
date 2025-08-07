"""Agent telemetry for tracking anonymous usage and feature usage."""

from core.telemetry import (
    record_event,
    increment as increment_counter,
    get_telemetry_client,
    flush,
    is_telemetry_enabled,
    is_telemetry_globally_disabled,
)

import platform

SYSTEM_INFO = {
    "os": platform.system().lower(),
    "os_version": platform.release(),
    "python_version": platform.python_version(),
}

__all__ = [
    "record_event",
    "increment_counter",
    "get_telemetry_client",
    "flush",
    "is_telemetry_enabled",
    "is_telemetry_globally_disabled",
    "SYSTEM_INFO",
]