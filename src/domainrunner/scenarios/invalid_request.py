"""Invalid Request Scenario.

Steps:
1. Send INTENT that provokes Provider Error (e.g. empty message)
2. Wait for processing
3. Fetch results

Expected:
INTENT -> DECISION(ALLOW) -> EXECUTION(ERROR)
"""
import time
import uuid

from domainrunner.client import GatewayClient
from domainrunner.observer_client import ObserverClient


def run() -> dict:
    gw = GatewayClient()
    obs = ObserverClient()
    
    thread_id = f"dr-invalid-{uuid.uuid4().hex[:6]}"
    
    # 1. Send intent with empty message to provoke Provider 400
    # Note: Gateway accepts it (Ingress), Policy allows it (if allow_all),
    # but Provider should reject empty prompts.
    try:
        gw.send_intent(
            thread_id=thread_id,
            message="",  # Empty message usually provokes 400
            actor="domainrunner-invalid",
        )
    except Exception as e:
        # If Ingress rejects it immediately, we might not get a ledger entry.
        # This demonstrates "Ingress Rejection" which is also valid governance,
        # but less interesting for the ledger demo.
        return {
            "scenario": "invalid_request",
            "thread_id": thread_id,
            "error": f"Ingress rejected request: {str(e)}",
            "events": [],
            "projection": None,
            "signals": [],
        }
    
    # 2. Wait
    time.sleep(1.0)
    
    # 3. Fetch
    raw_events = gw.get_snapshot(thread_id=thread_id, limit=500)
    projection = obs.get_thread(thread_id)
    signals = obs.get_signals()
    
    return {
        "scenario": "invalid_request",
        "thread_id": thread_id,
        "events": raw_events,
        "projection": projection,
        "signals": signals,
    }
