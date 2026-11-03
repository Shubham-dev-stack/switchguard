import pytest
from notifier.dispatcher import WebhookDispatcher, DispatchFailureError

def test_dispatcher_success():
    dispatcher = WebhookDispatcher()
    payload = {"content": "🚨 [P0] Incident Alert"}
    ok = dispatcher.dispatch("https://discord.com/api/webhooks/mock", payload)
    assert ok is True
    assert len(dispatcher.sent_history) == 1
    assert dispatcher.sent_history[0]["attempts"] == 1

def test_dispatcher_retry_and_recover():
    dispatcher = WebhookDispatcher(max_retries=3, backoff_factor=0.01)
    call_count = 0

    def flaky_transport(url, data):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ConnectionResetError("Connection dropped")
        return True

    payload = {"text": "Alert"}
    ok = dispatcher.dispatch("https://hooks.slack.com/services/mock", payload, transport_fn=flaky_transport)
    assert ok is True
    assert call_count == 2
    assert dispatcher.sent_history[0]["attempts"] == 2

def test_dispatcher_max_retries_exceeded():
    dispatcher = WebhookDispatcher(max_retries=2, backoff_factor=0.01)

    def fatal_transport(url, data):
        raise ConnectionRefusedError("Unreachable")

    with pytest.raises(DispatchFailureError):
        dispatcher.dispatch("https://downstream.api/webhook", {}, transport_fn=fatal_transport)
