import logging

from fastapi import APIRouter, HTTPException

from storeapi.errors import Duplicate, Missing
from storeapi.models.post import Comment, UserPost, UserPostIn, UserPostWithComments
from storeapi.services import post as service

router = APIRouter()

logger = logging.getLogger(__name__)


# structured via services: offload logic to services
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    try:
        return await service.create_post(post)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.get("/post", response_model=list[UserPost])
async def get_all_post():
    logger.info("Getting all post")
    try:
        return await service.get_all_post()
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comment_on_post(post_id: int):
    logger.info(f"Getting comments on post {post_id}")
    try:
        return await service.find_post_comment(post_id)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    ####


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comment(post_id: int):
    logger.info(f"Getting post {post_id} and its comments")
    try:
        post =  await service.find_post(post_id)
        comment = await get_comment_on_post(post_id)
        return {"post": post, "comment": comment}        
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
