import asyncio
import logging

from fastapi import APIRouter, Response

router = APIRouter()

logger = logging.getLogger(__name__)


# structured via services: offload logic to services
@router.get("/slow")
async def slow():
  await asyncio.sleep(10)
  return Response(content="OK", media_type="text/plain")

@router.get("/test", response_model=dict)
async def test():
  return {"msg": "Hello World!!!"}
