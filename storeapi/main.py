import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from prometheus_client import Counter, generate_latest

from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.comment import router as comment_router
from storeapi.routers.post import router as post_router

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
    header_name='X-Request-ID',
    update_request_header=True,
    generator=lambda: str(uuid4()),
    transformer=lambda a: a,
)
app.include_router(post_router)
app.include_router(comment_router)

### expose Counter based on /path
http_requests_total = Counter(
    'http_requests_total', 'Total number of HTTP requests', ['method', 'path']
)
@app.get("/metrics")
async def get_metrics():
    metrics = generate_latest()
    return Response(content=metrics, media_type="text/plain; version=0.0.4")

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    # Before request processing
    response = await call_next(request)
    
    # Increment the counter for the current path and method
    http_requests_total.labels(method=request.method, path=request.url.path).inc()

    return response

@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)