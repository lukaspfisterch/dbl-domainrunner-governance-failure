"""Bridge Service.

Synchronizes Gateway events to Observer.
This simulates the 'infrastructure' that ensures the Observer is up to date.
"""
import time
import os
import httpx
from rich.console import Console

console = Console()

def run_bridge():
    gateway_url = os.getenv("DBL_GATEWAY_URL", "http://127.0.0.1:8010").rstrip("/")
    observer_url = os.getenv("DBL_OBSERVER_URL", "http://127.0.0.1:8020").rstrip("/")
    
    console.print(f"[bold blue]Starting DBL Bridge[/]")
    console.print(f"Gateway:  {gateway_url}")
    console.print(f"Observer: {observer_url}")
    console.print()
    
    last_processed_index = -1
    
    while True:
        try:
            # 1. Fetch from Gateway
            # We fetch all (limit=500 is a demo simplification)
            # In production, we would use tails/cursors.
            resp = httpx.get(f"{gateway_url}/snapshot?limit=500")
            if resp.status_code != 200:
                time.sleep(1)
                continue
                
            data = resp.json()
            events = data.get("events", [])
            
            if not events:
                time.sleep(1)
                continue
                
            # 2. Push to Observer
            # The observer handles idempotency, so we can just push the snapshot
            resp = httpx.post(f"{observer_url}/ingest", json=data)
            
            if resp.status_code in (200, 202):
                new_count = len(events)
                if new_count > last_processed_index + 1:
                   console.print(f"[green]Synced {new_count} events[/]")
                   last_processed_index = new_count - 1
            else:
                console.print(f"[red]Observer connect failed: {resp.text}[/]")

        except Exception as e:
            # console.print(f"[dim]Sync error: {e}[/]")
            pass
            
        time.sleep(2)

if __name__ == "__main__":
    run_bridge()
