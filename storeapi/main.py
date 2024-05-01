from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware
from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.post import router as post_router


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
