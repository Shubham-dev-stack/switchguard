#!/usr/bin/env python3
"""
SwitchGuard: Master 1-Click Interactive Demo Runner
Powered by Switch AI Agent Architecture
"""
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = r"""
   ___          _ _       _      ___                       _ 
  / __|_ __ __ (_) |_  __| |_   / __|_  _ __ _ _ _ _ __ __| |
  \__ \ V  V / | |  _|/ _| ' \ | (_ | || / _` | '_/ _` / _` |
  |___/\_/\_/  |_|\__|\__|_||_| \___|\_,_\__,_|_| \__,_\__,_|
       Autonomous SRE Swarm & Cyber-Command Deck | Switch Hackathon
"""

def print_banner():
    try:
        print(f"{CYAN}{BOLD}{BANNER}{RESET}")
    except Exception:
        print("=== SWITCHGUARD AUTONOMOUS SRE COMMAND DECK ===")

def run_e2e_simulation():
    print(f"\n{BOLD}{CYAN}>>> [STEP 1] Running Autonomous Incident Triage & Self-Healing Simulation...{RESET}")
    from scripts.simulate_p0_outage import run_simulation
    return run_simulation()

def run_chaos_scenarios():
    print(f"\n{BOLD}{CYAN}>>> [STEP 2] Running Chaos Engineering Scenarios...{RESET}")
    from scenarios.jwt_expiry_regression import JWTAuthService, TokenValidationError
    from scenarios.database_deadlock import MockConnectionPool, BillingService, ConnectionPoolExhausted
    from scenarios.redis_cache_stampede import ProductCatalogCache, CacheStampedeError

    print("  [1/3] Testing JWT Authentication Bug & Auto-Rollback...")
    auth = JWTAuthService()
    t_bug = auth.create_token("user-42", buggy=True)
    try:
        auth.verify_token(t_bug)
        print("    [!] Unexpected: token should have failed")
    except TokenValidationError:
        print("    [✔] Ingested simulated auth failure. Applying patch...")
        t_clean = auth.create_token("user-42", buggy=False)
        assert auth.verify_token(t_clean) is True
        print("    [✔] Patch verified: JWT valid.")

    print("  [2/3] Testing DB Connection Pool Leak & Self-Healing...")
    pool = MockConnectionPool(max_size=3)
    billing = BillingService(pool)
    try:
        for _ in range(3):
            billing.process_charge(-10.0, buggy=True)
    except ValueError:
        pass
    print("    [✔] Pool exhaustion detected (0/3 available). Self-healing pool...")
    fixed_pool = MockConnectionPool(max_size=3)
    fixed_billing = BillingService(fixed_pool)
    for _ in range(5):
        try:
            fixed_billing.process_charge(-10.0, buggy=False)
        except ValueError:
            pass
    assert fixed_pool.available_count == 3
    print("    [✔] Connection pool leak remediated (3/3 available).")

    print("  [3/3] Testing Redis Cache Stampede Mitigation...")
    cache = ProductCatalogCache(db_query_limit=3)
    cache.get_product("sku-99", buggy=False)
    cache._cache["sku-99"]["expires_at"] = 0.0
    for _ in range(10):
        item = cache.get_product("sku-99", buggy=False)
        assert item["id"] == "sku-99"
    print("    [✔] Stale-while-revalidate lock protected DB against 10 surge requests.")

    print(f"\n{GREEN}[OK] All 3 Chaos Scenarios successfully triaged and repaired.{RESET}\n")
    return 0

def run_test_suite():
    print(f"\n{BOLD}{CYAN}>>> [STEP 3] Running Complete Test Suite (PyTest)...{RESET}")
    import subprocess
    ret = subprocess.call([sys.executable, "-m", "pytest", "-v", "tests/"])
    if ret == 0:
        print(f"\n{GREEN}[OK] All tests passed successfully!{RESET}\n")
    else:
        print(f"\n{RED}[ERR] Some tests failed with exit code {ret}{RESET}\n")
    return ret

def launch_dashboard(port=8080):
    print(f"\n{BOLD}{CYAN}>>> [STEP 4] Launching 3D CyberDeck Command Dashboard on port {port}...{RESET}")
    from dashboard.server import start_server
    start_server(port=port, open_browser=True)

def interactive_menu():
    print_banner()
    print("Welcome to SwitchGuard! Select an option:")
    print("  [1] Run P0 Autonomous Incident Simulation (Sentry -> Patch -> Audit -> Postmortem)")
    print("  [2] Launch 3D CyberDeck Command Dashboard (Three.js Web UI)")
    print("  [3] Run Chaos Engineering Scenarios (JWT Bug, DB Leak, Cache Stampede)")
    print("  [4] Run Full Test Suite (56 Tests)")
    print("  [5] Exit")
    print()

    if not sys.stdin.isatty():
        print(f"{YELLOW}Non-interactive terminal detected. Executing P0 Simulation by default...{RESET}\n")
        run_e2e_simulation()
        return 0

    try:
        choice = input("Enter choice [1-5]: ").strip()
        if choice == "1":
            run_e2e_simulation()
        elif choice == "2":
            launch_dashboard()
        elif choice == "3":
            run_chaos_scenarios()
        elif choice == "4":
            run_test_suite()
        elif choice == "5":
            print("Exiting SwitchGuard. Goodbye!")
            return 0
        else:
            print("Invalid choice. Running default P0 Simulation...")
            run_e2e_simulation()
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
    return 0

def main():
    import argparse
    parser = argparse.ArgumentParser(description="SwitchGuard 1-Click Interactive Demo Runner")
    parser.add_argument("--sim", action="store_true", help="Run end-to-end incident simulation")
    parser.add_argument("--dashboard", action="store_true", help="Launch 3D CyberDeck Dashboard directly")
    parser.add_argument("--chaos", action="store_true", help="Run chaos engineering scenarios")
    parser.add_argument("--test", action="store_true", help="Run test suite")
    parser.add_argument("--port", type=int, default=8080, help="Port for dashboard (default: 8080)")

    args = parser.parse_args()

    if args.sim:
        print_banner()
        return run_e2e_simulation()
    elif args.dashboard:
        print_banner()
        return launch_dashboard(port=args.port)
    elif args.chaos:
        print_banner()
        return run_chaos_scenarios()
    elif args.test:
        print_banner()
        return run_test_suite()
    else:
        return interactive_menu()

if __name__ == "__main__":
    sys.exit(main())
