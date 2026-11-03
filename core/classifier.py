from typing import Dict, Any, List
from .models import Alert, Severity, BlastRadius

# Tier 1 mission-critical services whose failures default to high severity
TIER_1_SERVICES = {"payment-gateway", "checkout", "authentication", "order-processing", "database-primary"}
TIER_2_SERVICES = {"inventory", "notification", "search", "shipping-calculator"}

CRITICAL_ERROR_PATTERNS = [
    "zerodivisionerror",
    "connectionrefused",
    "deadlock",
    "outofmemory",
    "segmentationfault",
    "securityviolation",
    "dataprocessingerror"
]

class SeverityClassifier:
    """
    Intelligent incident triage classifier that estimates blast radius and
    assigns industry-standard P0-P3 severity scores.
    """

    @classmethod
    def classify(cls, alert: Alert, error_rate_pct: float = 100.0) -> Severity:
        service_lower = alert.service.lower()
        error_lower = alert.error_type.lower()
        msg_lower = alert.message.lower()

        # Check for critical crash signatures in Tier 1 services
        is_tier_1 = service_lower in TIER_1_SERVICES
        is_fatal_error = any(pattern in error_lower or pattern in msg_lower for pattern in CRITICAL_ERROR_PATTERNS)

        if is_tier_1 and (is_fatal_error or error_rate_pct >= 50.0):
            return Severity.P0_CRITICAL

        if is_tier_1 or (is_fatal_error and error_rate_pct >= 20.0):
            return Severity.P1_MAJOR

        if error_rate_pct >= 10.0 or service_lower in TIER_2_SERVICES:
            return Severity.P2_MODERATE

        return Severity.P3_LOW

    @classmethod
    def estimate_blast_radius(cls, alert: Alert, error_rate_pct: float, active_traffic_rps: float = 150.0) -> BlastRadius:
        severity = cls.classify(alert, error_rate_pct)
        
        # Financial loss estimate ($50 average order value per failed request on payment services)
        is_payment = "payment" in alert.service.lower() or "checkout" in alert.service.lower()
        estimated_lost_orders_per_minute = (active_traffic_rps * (error_rate_pct / 100.0)) * 60.0 if is_payment else 0.0
        financial_risk = round(estimated_lost_orders_per_minute * 50.0, 2)

        endpoints = [f"/{alert.service}/v1/process", f"/{alert.service}/health"]

        return BlastRadius(
            affected_users_pct=min(100.0, error_rate_pct),
            affected_endpoints=endpoints,
            financial_impact_estimate_usd=financial_risk,
            degraded_dependencies=[alert.service]
        )
