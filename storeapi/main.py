import logging
import time
from contextlib import asynccontextmanager
from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from prometheus_client import Summary, generate_latest

from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.comment import router as comment_router
from storeapi.routers.post import router as post_router
from storeapi.routers.test import router as test_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
    update_request_header=True,
    generator=lambda: str(uuid4()),
    transformer=lambda a: a,
)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(test_router)

def normalize_path(path: str) -> str:
    if path.startswith("/post/"):
        return "/post/{id}"
    return path

### expose Summary: based on /path
REQUEST_LATENCY = Summary(
    "http_request_latency_seconds",
    "Request latency in seconds",
    ["method", "path", "status_code"],
)


@app.get("/metrics")
async def get_metrics():
    metrics = generate_latest()
    return Response(content=metrics, media_type="text/plain")


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    # Record start-time, load request, so latency=now - start
    start_time = time.time()  # Record start time
    response = await call_next(request)
    request_latency = time.time() - start_time

    path = normalize_path(request.url.path)
    # Observe the request latency with method, path, and status_code as labels
    # exclude 404
    if response.status_code != 404:
        REQUEST_LATENCY.labels(
            method=request.method,
            path=path,
            status_code=str(response.status_code),
        ).observe(request_latency)
    return response


### End expose Summary


@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
