2026-01-19T13:44:51+01:00
# Inventory: dbl-domainrunner-governance-failure

## Tree

- pyproject.toml
- README.md
- src/domainrunner/__init__.py
- src/domainrunner/client.py
- src/domainrunner/main.py
- src/domainrunner/observer_client.py
- src/domainrunner/scenarios/__init__.py
- src/domainrunner/scenarios/happy_path.py
- src/domainrunner/scenarios/invalid_request.py
- src/domainrunner/visualizer.py

## File Contents

### pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "dbl-domainrunner-governance-failure"
version = "0.1.0"
description = "Domainrunner demo: witness AI governance failure and DBL prevention"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }

dependencies = [
  "httpx>=0.27",
  "rich>=13.0",
]

[project.scripts]
domainrunner = "domainrunner.main:main"

[tool.setuptools]
package-dir = { "" = "src" }

[tool.setuptools.packages.find]
where = ["src"]
include = ["domainrunner*"]

```

### README.md
```markdown
# dbl-domainrunner-governance-failure

**This Domainrunner is a witness, not a participant.**

---

## Purpose

Demonstrate, in a reproducible and concrete way, why AI governance fails even with good data when no deterministic boundary exists — and how DBL prevents that failure.

---

## What This Demo Shows

| Scenario | What Happens | What You See |
|----------|--------------|--------------|
| `happy_path` | INTENT → ALLOW → EXECUTION (success) | Clean audit trail |
| `invalid_request` | INTENT → ALLOW → EXECUTION (error: 400) | Failure correctly classified |
| ~~`policy_deny`~~ | *(Phase 2: requires policy pack)* | — |

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                      DOMAINRUNNER                              │
│  • Sends INTENTs to Gateway                                    │
│  • Reads events from Gateway /snapshot                         │
│  • Reads projections from Observer /threads, /signals          │
│  • DOES NOT write to Observer                                  │
│  • DOES NOT make decisions                                     │
│  • DOES NOT store authoritative state                          │
└────────────────────────────────────────────────────────────────┘
         │                                    │
         │ POST /ingress/intent               │ GET /threads (READ ONLY)
         │ GET /snapshot                      │ GET /signals (READ ONLY)
         ▼                                    ▼
┌─────────────────────┐              ┌─────────────────────┐
│    DBL-GATEWAY      │              │    DBL-OBSERVER     │
│   (NORMATIVE)       │              │   (NON_NORMATIVE)   │
│                     │              │                     │
│ • Emits DECISION    │              │ • Projects events   │
│ • Executes (or not) │              │ • Generates signals │
│ • Appends to ledger │              │ • Read-only API     │
└─────────────────────┘              └─────────────────────┘
```

### Communication Rules (HARD)

| From | To | Allowed |
|------|----|---------|
| Domainrunner → Gateway `/ingress/intent` | ✅ Write |
| Domainrunner → Gateway `/snapshot` | ✅ Read |
| Domainrunner → Observer `/threads`, `/signals` | ✅ Read |
| Domainrunner → Observer `/ingest` | ❌ **FORBIDDEN** |

---

## Quick Start (60 seconds)

### Prerequisites

```powershell
# Gateway running on localhost:8010
# Observer running on localhost:8020 (optional, for projections)
```

### Run Demo

```powershell
cd dbl-domainrunner-governance-failure

# Install
pip install -e .

# Run all Phase 1 scenarios
python -m domainrunner
```

### Expected Output

```
┌──────────────────────────────────────────────────────────────────┐
│ Scenario: invalid_request                                        │
│ Thread:   dr-invalid-001                                         │
├──────────────────────────────────────────────────────────────────┤
│ RAW LEDGER (Gateway /snapshot)                                   │
│ ─────────────────────────────────────────────────────────────────│
│  #0  INTENT      turn=t001  message="trigger 400"                │
│  #1  DECISION    result=ALLOW  reason=[allow_all]                │
│  #2  EXECUTION   status=ERROR  code=invalid_request_error        │
├──────────────────────────────────────────────────────────────────┤
│ PROJECTION (Observer /threads/dr-invalid-001)                    │
│ ─────────────────────────────────────────────────────────────────│
│  turns_total: 1                                                  │
│  allow_total: 1                                                  │
│  execution_error_total: 1                                        │
└──────────────────────────────────────────────────────────────────┘
```

---

## Why This Demo Matters

| Without DBL | With DBL |
|-------------|----------|
| "AI failed" (opaque) | DECISION: ALLOW, EXECUTION: ERROR (invalid_request) |
| "AI refused" (opaque) | DECISION: DENY, reason: [policy.X] |
| "AI worked" (opaque) | DECISION: ALLOW, EXECUTION: OK |

**The demo forces the viewer to see:**
- Each event has exactly one kind (INTENT, DECISION, EXECUTION)
- Responsibility is explicit (Gateway decided; Provider failed; Observer reported)
- Failure is classified, not guessed
- Replay is trivial

---

## Constraints (NON_NEGOTIABLE)

1. **No policy logic inside domainrunner**
2. **No decision inference**
3. **No state that claims to be authoritative**
4. **No writes to Observer**

---

## Phases

| Phase | Scenarios | Status |
|-------|-----------|--------|
| **1** | happy_path, invalid_request | ✅ Ready |
| **2** | policy_deny | Requires policy pack |



```

### src/domainrunner/__init__.py
```python
"""Domainrunner: Witness, not participant."""

```

### src/domainrunner/client.py
```python
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

```

### src/domainrunner/main.py
```python
"""Domainrunner Entrypoint."""
import sys
import time

from domainrunner.client import GatewayClient
from domainrunner.observer_client import ObserverClient
from domainrunner.scenarios import happy_path, invalid_request
from domainrunner.visualizer import (
    render_scenario_result,
    print_header,
    print_gateway_unreachable,
    print_observer_unavailable,
)


def main():
    print_header()
    
    # 1. Health Check
    gw = GatewayClient()
    obs = ObserverClient()
    
    try:
        gw.get_status()
    except Exception:
        print_gateway_unreachable(gw.base_url)
        sys.exit(1)
        
    if not obs.is_available():
        print_observer_unavailable()

    # 2. Run Scenarios
    scenarios = [
        happy_path,
        invalid_request,
    ]
    
    for i, scenario in enumerate(scenarios):
        if i > 0:
            time.sleep(1) # Visual separator pause
        
        try:
            result = scenario.run()
            render_scenario_result(result)
        except Exception as e:
            # Fallback if scenario code crashes
            from rich.console import Console
            Console().print_exception()

    # 3. Done
    print("\n[dim]Done.[/]")


if __name__ == "__main__":
    main()

```

### src/domainrunner/observer_client.py
```python
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

```

### src/domainrunner/scenarios/__init__.py
```python
"""Scenarios package."""

```

### src/domainrunner/scenarios/happy_path.py
```python
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

```

### src/domainrunner/scenarios/invalid_request.py
```python
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

```

### src/domainrunner/visualizer.py
```python
"""Visualizer: Render audit trail and projections.

This module renders data to the terminal using Rich.
It displays, never interprets.
"""
from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


def render_scenario_result(result: dict[str, Any]) -> None:
    """Render a complete scenario result with all panels."""
    scenario = result.get("scenario", "unknown")
    thread_id = result.get("thread_id", "unknown")
    events = result.get("events", [])
    projection = result.get("projection")
    signals = result.get("signals", [])
    error = result.get("error")

    # Header
    console.print()
    console.rule(f"[bold blue]Scenario: {scenario}[/]")
    console.print(f"[dim]Thread: {thread_id}[/]")
    console.print()

    if error:
        console.print(Panel(f"[red]{error}[/]", title="Error", border_style="red"))
        return

    # Panel A: Raw Ledger
    _render_raw_ledger(events)

    # Panel B: Projection (if available)
    if projection:
        _render_projection(projection)

    # Panel C: Signals (if any)
    _render_signals(signals)

    console.print()


def _render_raw_ledger(events: list[dict[str, Any]]) -> None:
    """Render raw events from gateway snapshot."""
    table = Table(title="RAW LEDGER (Gateway /snapshot)", box=None, padding=(0, 1))
    table.add_column("#", style="dim", width=4)
    table.add_column("Kind", style="bold", width=12)
    table.add_column("Turn ID", width=20)
    table.add_column("Details", style="dim")

    for i, event in enumerate(events):
        kind = event.get("kind", "?")
        turn_id = event.get("turn_id", "?")[:20]
        
        # Kind-specific styling
        if kind == "INTENT":
            kind_styled = f"[cyan]{kind}[/]"
            details = _extract_intent_details(event)
        elif kind == "DECISION":
            result = event.get("payload", {}).get("decision", "?")
            if result == "ALLOW":
                kind_styled = f"[green]{kind}[/]"
            else:
                kind_styled = f"[red]{kind}[/]"
            details = f"result={result}"
        elif kind == "EXECUTION":
            payload = event.get("payload", {})
            if "error" in payload:
                kind_styled = f"[red]{kind}[/]"
                err = payload.get("error", {})
                details = f"ERROR: {err.get('code', err.get('message', '?'))}"
            else:
                kind_styled = f"[green]{kind}[/]"
                details = "status=OK"
        else:
            kind_styled = kind
            details = ""
        
        table.add_row(str(i), kind_styled, turn_id, details)

    console.print(Panel(table, border_style="blue"))


def _extract_intent_details(event: dict[str, Any]) -> str:
    """Extract readable details from INTENT event."""
    payload = event.get("payload", {})
    message = payload.get("message", payload.get("user_input", ""))
    if len(message) > 40:
        message = message[:37] + "..."
    return f'message="{message}"'


def _render_projection(projection: dict[str, Any]) -> None:
    """Render observer projection."""
    thread = projection.get("thread", {})
    turns = projection.get("turns", [])

    text = Text()
    text.append(f"turns_total: {thread.get('turns_total', 0)}\n")
    text.append(f"allow_total: {thread.get('allow_total', 0)}\n")
    text.append(f"deny_total: {thread.get('deny_total', 0)}\n")
    text.append(f"execution_error_total: {thread.get('execution_error_total', 0)}\n")
    
    if turns:
        text.append(f"\nTurns: {len(turns)}")

    console.print(Panel(text, title="PROJECTION (Observer /threads/{id})", border_style="green"))


def _render_signals(signals: list[dict[str, Any]]) -> None:
    """Render signals (if any)."""
    if not signals:
        console.print(Panel("[dim](no signals - insufficient data for thresholds)[/]", 
                           title="SIGNALS (NON_NORMATIVE)", border_style="yellow"))
        return

    table = Table(title="SIGNALS (NON_NORMATIVE)", box=None)
    table.add_column("Severity", width=10)
    table.add_column("ID", width=30)
    table.add_column("Title")

    for signal in signals:
        severity = signal.get("severity", "?")
        if severity == "critical":
            sev_styled = f"[red bold]{severity}[/]"
        elif severity == "warn":
            sev_styled = f"[yellow]{severity}[/]"
        else:
            sev_styled = f"[dim]{severity}[/]"
        
        table.add_row(sev_styled, signal.get("id", "?"), signal.get("title", "?"))

    console.print(Panel(table, border_style="yellow"))


def print_header() -> None:
    """Print demo header."""
    console.print()
    console.print(Panel.fit(
        "[bold]DBL Domainrunner: Governance Failure Demo[/]\n"
        "[dim]This domainrunner is a witness, not a participant.[/]",
        border_style="blue",
    ))
    console.print()


def print_gateway_unreachable(url: str) -> None:
    """Print gateway unreachable error."""
    console.print(Panel(
        f"[red]Gateway not reachable at {url}[/]\n\n"
        "Start the gateway first:\n"
        "[dim]dbl-gateway[/]",
        title="Error",
        border_style="red",
    ))


def print_observer_unavailable() -> None:
    """Print observer unavailable notice."""
    console.print("[dim]Observer not available - skipping projections[/]")

```
