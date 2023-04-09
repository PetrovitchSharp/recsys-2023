from time import time

from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from prometheus_client.core import CollectorRegistry


def add_prometheus_middleware(app: FastAPI):
    registry = CollectorRegistry()
    REQUEST_COUNT = Counter(
        "request_count", "App Request Count", registry=registry
    )
    REQUEST_LATENCY = Histogram(
        "request_latency_seconds", "Request latency", registry=registry
    )
    REQUEST_IN_PROGRESS = Gauge(
        "requests_in_progress",
        "Count of requests in progress",
        registry=registry,
    )

    @app.middleware("http")
    async def monitor_requests(request: Request, call_next):
        REQUEST_IN_PROGRESS.inc()

        start_time = time()
        response = await call_next(request)
        latency = time() - start_time

        REQUEST_IN_PROGRESS.dec()

        REQUEST_LATENCY.observe(latency)

        REQUEST_COUNT.inc()

        return response

    @app.get("/metrics")
    async def get_metrics():
        """Prometheus endpoint"""
        return Response(
            generate_latest(registry), media_type=CONTENT_TYPE_LATEST
        )
