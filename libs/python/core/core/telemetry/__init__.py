"""This module provides the core telemetry functionality for CUA libraries.

It provides a low-overhead way to collect anonymous usage data.
"""

from core.telemetry.telemetry import (
    flush,
    increment,
    record_event,
    is_telemetry_enabled,
    destroy_telemetry_client,
)


__all__ = [
    "flush",
    "increment",
    "record_event",
    "is_telemetry_enabled",
    "destroy_telemetry_client",
]
