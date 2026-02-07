"""
Load test Tools API – pytest.

Gửi nhiều request đồng thời tới Tools (health, interest, savings-rate), đo latency và RPS.
Chạy: pytest tests/load/test_load_tools.py -v -s
      TOOLS_URL=http://localhost:8081 pytest tests/load/test_load_tools.py -v -s
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
import httpx

TOOLS_URL = os.getenv("TOOLS_URL", "http://localhost:8081").rstrip("/")
NUM_REQUESTS = int(os.getenv("LOAD_NUM_REQUESTS", "50"))
NUM_WORKERS = int(os.getenv("LOAD_NUM_WORKERS", "10"))
TIMEOUT = 10.0


def _get_health() -> tuple[float, int]:
    start = time.perf_counter()
    r = httpx.get(f"{TOOLS_URL}/health", timeout=TIMEOUT)
    elapsed = time.perf_counter() - start
    return elapsed, r.status_code


def _post_interest() -> tuple[float, int]:
    start = time.perf_counter()
    r = httpx.post(
        f"{TOOLS_URL}/tools/interest",
        json={"principal": 100_000_000, "rate_percent": 6, "months": 12},
        timeout=TIMEOUT,
    )
    elapsed = time.perf_counter() - start
    return elapsed, r.status_code


def _post_savings_rate() -> tuple[float, int]:
    start = time.perf_counter()
    r = httpx.post(
        f"{TOOLS_URL}/tools/savings-rate",
        json={"income": 20_000_000, "savings": 4_000_000},
        timeout=TIMEOUT,
    )
    elapsed = time.perf_counter() - start
    return elapsed, r.status_code


@pytest.mark.skipif(
    os.getenv("SKIP_LOAD_TEST") == "1",
    reason="Bỏ qua load test (set SKIP_LOAD_TEST=1 để skip)",
)
def test_load_tools_health() -> None:
    """Nhiều request GET /health đồng thời."""
    latencies: list[float] = []
    codes: list[int] = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as ex:
        futures = [ex.submit(_get_health) for _ in range(NUM_REQUESTS)]
        for f in as_completed(futures):
            elapsed, code = f.result()
            latencies.append(elapsed)
            codes.append(code)
    ok = sum(1 for c in codes if c == 200)
    avg_ms = (sum(latencies) / len(latencies)) * 1000
    rps = NUM_REQUESTS / sum(latencies) if latencies else 0
    print(f"\n[Tools /health] requests={NUM_REQUESTS}, ok={ok}, avg_ms={avg_ms:.1f}, rps={rps:.1f}")
    assert ok == NUM_REQUESTS, f"Expected all 200, got {codes[:10]}..."


@pytest.mark.skipif(
    os.getenv("SKIP_LOAD_TEST") == "1",
    reason="Bỏ qua load test",
)
def test_load_tools_interest() -> None:
    """Nhiều request POST /tools/interest đồng thời."""
    latencies = []
    codes = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as ex:
        futures = [ex.submit(_post_interest) for _ in range(NUM_REQUESTS)]
        for f in as_completed(futures):
            elapsed, code = f.result()
            latencies.append(elapsed)
            codes.append(code)
    ok = sum(1 for c in codes if c == 200)
    avg_ms = (sum(latencies) / len(latencies)) * 1000
    rps = NUM_REQUESTS / sum(latencies) if latencies else 0
    print(f"\n[Tools /interest] requests={NUM_REQUESTS}, ok={ok}, avg_ms={avg_ms:.1f}, rps={rps:.1f}")
    assert ok == NUM_REQUESTS
