from typing import Dict, Any, Optional
from core.models import Alert

class SentryWebhookParser:
    """
    Parses Sentry issue alert webhooks into normalized SwitchGuard Alert objects.
    """

    @classmethod
    def parse(cls, payload: Dict[str, Any]) -> Alert:
        event = payload.get("data", {}).get("event", {})
        metadata = payload.get("data", {}).get("issue", {}).get("metadata", {})
        project_slug = payload.get("data", {}).get("issue", {}).get("project", {}).get("slug", "unknown-service")
        
        event_id = event.get("event_id", payload.get("id", "SENTRY-EVT"))
        error_type = metadata.get("type", "RuntimeError")
        message = metadata.get("value", event.get("title", "Unhandled error from Sentry"))
        
        # Extract stack trace if available
        stack_trace = None
        entries = event.get("entries", [])
        for entry in entries:
            if entry.get("type") == "exception":
                values = entry.get("data", {}).get("values", [])
                if values and "stacktrace" in values[0]:
                    frames = values[0]["stacktrace"].get("frames", [])
                    if frames:
                        last_frame = frames[-1]
                        stack_trace = f"{last_frame.get('filename')}:{last_frame.get('lineno')} in {last_frame.get('function')}"

        return Alert(
            alert_id=f"SENTRY-{event_id}",
            source="sentry",
            service=project_slug,
            error_type=error_type,
            message=message,
            stack_trace=stack_trace,
            metadata={"sentry_url": payload.get("url", "")}
        )


class DatadogWebhookParser:
    """
    Parses Datadog webhook monitor payloads into normalized SwitchGuard Alert objects.
    """

    @classmethod
    def parse(cls, payload: Dict[str, Any]) -> Alert:
        alert_id = str(payload.get("id", "DATADOG-EVT"))
        title = payload.get("event_title", "Datadog Monitor Alert")
        body = payload.get("body", "")
        tags = payload.get("tags", "")
        
        # Derive service name from tags (e.g. "service:checkout,env:prod")
        service = "unknown-service"
        if isinstance(tags, str):
            for t in tags.split(","):
                if t.strip().startswith("service:"):
                    service = t.strip().split(":", 1)[1]
        elif isinstance(tags, list):
            for t in tags:
                if t.startswith("service:"):
                    service = t.split(":", 1)[1]

        return Alert(
            alert_id=f"DD-{alert_id}",
            source="datadog",
            service=service,
            error_type="MetricThresholdBreach",
            message=f"{title}: {body}",
            metadata={"priority": payload.get("priority", "normal")}
        )


class PrometheusAlertmanagerParser:
    """
    Parses Prometheus Alertmanager webhook payloads.
    """

    @classmethod
    def parse(cls, payload: Dict[str, Any]) -> Alert:
        alerts = payload.get("alerts", [])
        first_alert = alerts[0] if alerts else {}
        labels = first_alert.get("labels", {})
        annotations = first_alert.get("annotations", {})

        service = labels.get("job", labels.get("service", "cluster-node"))
        alertname = labels.get("alertname", "PrometheusAlert")
        summary = annotations.get("summary", annotations.get("description", "High error rate or resource exhaustion"))

        return Alert(
            alert_id=f"PROM-{labels.get('instance', 'node')}-{alertname}",
            source="prometheus",
            service=service,
            error_type=alertname,
            message=summary,
            metadata={"severity": labels.get("severity", "critical")}
        )
