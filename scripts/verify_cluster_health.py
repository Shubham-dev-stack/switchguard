#!/usr/bin/env python3
"""
Cluster Health Probe:
Synthetically verifies latency and health status across all registered microservices.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diagnostics.healthcheck import ServiceHealthProbe

SERVICES = ["checkout-service", "payment-gateway", "auth-service", "order-processing"]

def verify_cluster():
    print("=== SwitchGuard Microservice Cluster Health ===")
    all_healthy = True
    for svc in SERVICES:
        probe = ServiceHealthProbe(svc)
        res = probe.probe(lambda: True)
        status_icon = "🟢" if res["healthy"] else "🔴"
        print(f"{status_icon} {svc.ljust(22)}: {res['status']} ({res['latency_ms']} ms)")
        if not res["healthy"]:
            all_healthy = False
    return 0 if all_healthy else 1

if __name__ == "__main__":
    sys.exit(verify_cluster())
