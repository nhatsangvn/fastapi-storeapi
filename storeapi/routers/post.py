import logging

from fastapi import APIRouter, HTTPException

from storeapi.database import comment_table, database, post_table
from storeapi.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()

logger = logging.getLogger(__name__)


async def find_post(post_id: int):
    logger.info(f"Finding post {post_id}")

    query = post_table.select().where(post_table.c.id == post_id)

    logger.debug(query)
    return await database.fetch_one(query)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    logger.info("Creating post")

    data = post.model_dump()

    query = post_table.insert().values(data)

    # new_post = {**data, "id": last_record_id}
    logger.debug(query)storeapi
    last_record_id = await database.execute(query)

    return {**data, "id": last_record_id}


@router.get("/post", response_model=list[UserPost])
async def get_all_post():
    logger.info("Getting all post")

    query = post_table.select()

    logger.debug(query)
    return await database.fetch_all(query)


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    logger.info(f"Creating comment on post {comment.post_id}")

    post = await find_post(comment.post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    query = comment_table.insert().values(data)

    logger.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comment_on_post(post_id: int):
    logger.info(f"Getting comments on post {post_id}")

    post = await find_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    query = comment_table.select().where(comment_table.c.post_id == post_id)

    logger.debug(query)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comment(post_id: int):
    logger.info(f"Getting post {post_id} and its comments")

    post = await find_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comment": await get_comment_on_post(post_id)
    }
