from time import time

import psutil
from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from prometheus_client.core import CollectorRegistry


def add_prometheus_middleware(app: FastAPI):
    registry = CollectorRegistry()
    REQUEST_COUNT = Counter("request_count", "App Request Count", registry=registry)
    RESPONSE_TIME = Histogram("response_time", "Response time", registry=registry)
    CPU_USAGE = Gauge("cpu_usage", "CPU usage", registry=registry)
    MEMORY_USAGE = Gauge("memory_usage", "Memory usage", registry=registry)

    @app.middleware("http")
    async def monitor_requests(request: Request, call_next):
        REQUEST_COUNT.inc()

        start_time = time()
        response = await call_next(request)
        latency = time() - start_time

        RESPONSE_TIME.observe(latency)

        return response

    @app.get("/metrics")
    async def get_metrics():
        """Prometheus endpoint"""
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(psutil.virtual_memory().used / 1024 / 1024 / 1024)

        return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
