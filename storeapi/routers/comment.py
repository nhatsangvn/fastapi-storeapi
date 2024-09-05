import logging

from fastapi import APIRouter, HTTPException

from storeapi.errors import Duplicate, Missing
from storeapi.models.post import Comment, CommentIn
from storeapi.services import comment as service

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    logger.info(f"Creating comment on post {comment.post_id}")
    
    try:
        return await service.create_comment(comment)    
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

