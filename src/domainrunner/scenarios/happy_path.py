"""Happy Path Scenario.

Steps:
1. Send valid INTENT
2. Wait for processing
3. Fetch results

Expected:
INTENT -> DECISION(ALLOW) -> EXECUTION(OK)
"""
import time
import uuid

from domainrunner.client import GatewayClient
from domainrunner.observer_client import ObserverClient


def run() -> dict:
    gw = GatewayClient()
    obs = ObserverClient()
    
    thread_id = f"dr-happy-{uuid.uuid4().hex[:6]}"
    
    # 1. Send intent
    gw.send_intent(
        thread_id=thread_id,
        message="Hello from domainrunner happy path",
        actor="domainrunner-happy",
    )
    
    # 2. Wait for processing (Gateway is async)
    time.sleep(1.0)
    
    # 3. Fetch results
    # Pass 'limit=500' to ensure we get our events if ledger is busy
    raw_events = gw.get_snapshot(thread_id=thread_id, limit=500)
    
    projection = obs.get_thread(thread_id)
    signals = obs.get_signals()
    
    return {
        "scenario": "happy_path",
        "thread_id": thread_id,
        "events": raw_events,
        "projection": projection,
        "signals": signals,
    }
