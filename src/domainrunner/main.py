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
