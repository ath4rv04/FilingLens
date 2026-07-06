import time
from filinglens.utils.timer import Timer, request_id_ctx_var


def test_timer_captures_execution():
    request_id_ctx_var.set("test_timer_123")

    with Timer("mock_test") as t:
        time.sleep(0.01)

    assert t.elapsed_ms > 0
    assert t.name == "mock_test"
