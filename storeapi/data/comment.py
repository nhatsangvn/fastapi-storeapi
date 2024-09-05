import logging

from storeapi.database import comment_table, database
from storeapi.models.post import CommentIn

logger = logging.getLogger(__name__)

async def create_comment(comment: CommentIn):
    data = comment.model_dump()

    query = comment_table.insert().values(data)

    logger.debug(query)
    last_record_id = await database.execute(query)

    return last_record_id


async def get_comment_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)

    logger.debug(query)
    return await database.fetch_all(query)