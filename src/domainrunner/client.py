"""Gateway HTTP client.

This module provides a minimal HTTP client for the DBL Gateway.
It ONLY sends INTENTs and reads snapshots. No decision logic.
"""
from __future__ import annotations

import os
import uuid
from typing import Any

import httpx


class GatewayClient:
    """HTTP client for DBL Gateway.
    
    Responsibilities:
    - POST /ingress/intent (send intent)
    - GET /snapshot (read ledger)
    
    Non-responsibilities:
    - No decision logic
    - No state storage
    - No interpretation
    """

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("DBL_GATEWAY_URL", "http://127.0.0.1:8010")).rstrip("/")

    def send_intent(
        self,
        *,
        thread_id: str,
        message: str,
        turn_id: str | None = None,
        actor: str = "domainrunner",
    ) -> dict[str, Any]:
        """Send an intent to the gateway.
        
        Returns the gateway response (usually 202 Accepted with correlation info).
        """
        payload = {
            "thread_id": thread_id,
            "turn_id": turn_id or f"turn-{uuid.uuid4().hex[:8]}",
            "actor": actor,
            "intent_type": "chat.message",
            "payload": {
                "message": message,
            },
        }
        
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(f"{self.base_url}/ingress/intent", json=payload)
            resp.raise_for_status()
            return resp.json()

    def get_snapshot(
        self,
        *,
        thread_id: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Fetch raw events from gateway ledger.
        
        Returns list of events in ledger order.
        """
        params: dict[str, Any] = {"limit": limit}
        if thread_id:
            params["stream_id"] = "default"  # Gateway uses stream_id
        
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{self.base_url}/snapshot", params=params)
            resp.raise_for_status()
            data = resp.json()
            events = data.get("events", [])
            
            # Filter by thread_id if specified
            if thread_id:
                events = [e for e in events if e.get("thread_id") == thread_id]
            
            return events

    def get_status(self) -> dict[str, Any]:
        """Fetch gateway status."""
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{self.base_url}/status")
            resp.raise_for_status()
            return resp.json()
