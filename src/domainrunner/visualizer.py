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
        console.print(Panel("[dim](no signals - insufficient data for thresholds)[/]\n[italic dim]These signals do NOT affect decisions. They indicate patterns, not authority.[/]", 
                           title="SIGNALS (NON_NORMATIVE)", border_style="yellow"))
        return

    table = Table(title="SIGNALS (NON_NORMATIVE)", box=None, caption="[italic dim]These signals do NOT affect decisions. They indicate patterns, not authority.[/]")
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
