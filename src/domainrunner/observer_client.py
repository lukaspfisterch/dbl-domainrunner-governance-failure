"""Observer HTTP client.

This module provides a READ-ONLY client for the DBL Observer.
It reads projections and signals. NEVER writes.

INVARIANT: Domainrunner does NOT call /ingest.
"""
from __future__ import annotations

import os
from typing import Any

import httpx


class ObserverClient:
    """HTTP client for DBL Observer (READ-ONLY).
    
    Responsibilities:
    - GET /threads (read thread projections)
    - GET /threads/{id} (read single thread)
    - GET /signals (read attention markers)
    - GET /status (read system metrics)
    
    FORBIDDEN:
    - POST /ingest (would make us a participant, not witness)
    """

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("DBL_OBSERVER_URL", "http://127.0.0.1:8020")).rstrip("/")

    def get_threads(self) -> list[dict[str, Any]]:
        """Fetch all thread summaries."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/threads")
            if resp.status_code == 200:
                return resp.json().get("threads", [])
            return []

    def get_thread(self, thread_id: str) -> dict[str, Any] | None:
        """Fetch single thread summary with turns."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/threads/{thread_id}")
            if resp.status_code == 200:
                return resp.json()
            return None

    def get_signals(self) -> list[dict[str, Any]]:
        """Fetch current signals (NON_NORMATIVE attention markers)."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/signals")
            if resp.status_code == 200:
                return resp.json().get("signals", [])
            return []

    def get_status(self) -> dict[str, Any] | None:
        """Fetch observer status."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/status")
            if resp.status_code == 200:
                return resp.json()
            return None

    def is_available(self) -> bool:
        """Check if observer is reachable."""
        try:
            with httpx.Client(timeout=2.0) as client:
                resp = client.get(f"{self.base_url}/healthz")
                return resp.status_code == 200
        except httpx.RequestError:
            return False
