"""Lightweight telemetry wrapper for PostHog. All helpers are thin wrappers around
a single, lazily-initialised PostHog client.

Usage:
    from core.telemetry import record_event, increment

    record_event("my_event", {"foo": "bar"})

Configuration:
    • Disable telemetry globally by setting the environment variable
      CUA_TELEMETRY=off   OR   CUA_TELEMETRY_ENABLED=false/0.
    • Control log verbosity with CUA_TELEMETRY_LOG_LEVEL (DEBUG|INFO|WARNING|ERROR).

If the `posthog` package (and the accompanying `PostHogTelemetryClient` helper)
are not available, every public function becomes a no-op.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

_DEFAULT_LOG_LEVEL = os.environ.get("CUA_TELEMETRY_LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=getattr(logging, _DEFAULT_LOG_LEVEL, logging.WARNING))
_LOGGER = logging.getLogger("core.telemetry")

# ---------------------------------------------------------------------------
# Attempt to import the PostHog client helper. If unavailable, telemetry is
# silently disabled.
# ---------------------------------------------------------------------------

try:
    from core.telemetry.posthog_client import get_posthog_telemetry_client  # type: ignore
except ImportError:  # pragma: no cover
    get_posthog_telemetry_client = None  # type: ignore[misc, assignment]

# ---------------------------------------------------------------------------
# Internal helpers & primitives
# ---------------------------------------------------------------------------

def _telemetry_disabled() -> bool:
    """Return True if the user has disabled telemetry via environment vars."""
    return (
        os.environ.get("CUA_TELEMETRY", "").lower() == "off"  # legacy flag
        or os.environ.get("CUA_TELEMETRY_ENABLED", "true").lower()  # new flag
        not in {"1", "true", "yes", "on"}
    )


_CLIENT = None  # Lazily instantiated PostHog client instance
_ENABLED = False  # Guard to avoid making calls when telemetry disabled

def _ensure_client() -> None:
    """Initialise the PostHog client once and cache it globally."""
    global _CLIENT, _ENABLED

    # Bail early if telemetry is disabled or already initialised
    if _CLIENT is not None or _telemetry_disabled():
        return

    if get_posthog_telemetry_client is None:
        _LOGGER.debug("posthog package not found – telemetry disabled")
        return

    try:
        _CLIENT = get_posthog_telemetry_client()
        _ENABLED = True
    except Exception as exc:  # pragma: no cover
        _LOGGER.debug("Failed to initialise PostHog client: %s", exc)
        _CLIENT = None
        _ENABLED = False

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def destroy_telemetry_client() -> None:
    """Destroy the global telemetry client."""
    global _CLIENT
    _CLIENT = None

def is_telemetry_enabled() -> bool:
    """Return True if telemetry is currently active."""
    _ensure_client()
    return _ENABLED and not _telemetry_disabled()

def record_event(event_name: str, properties: Optional[Dict[str, Any]] | None = None) -> None:
    """Send an arbitrary PostHog event."""
    _ensure_client()
    if _CLIENT and _ENABLED:
        _CLIENT.record_event(event_name, properties or {})