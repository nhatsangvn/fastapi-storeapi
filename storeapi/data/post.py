import logging

logger = logging.getLogger(__name__)

from storeapi.database import database, post_table  # noqa: E402
from storeapi.errors import Missing
from storeapi.models.post import UserPostIn  # noqa: E402

# async def row_to_model(row: tuple) -> UserPost:
#     print(4)
#     id, body = tuple(row)
#     return UserPost(id=int(id), body=body)


# async def find_post(post_id: int) -> UserPost:
#     print(3)
#     logger.info(f"Finding post {post_id}")

#     query = post_table.select().where(post_table.c.id == post_id)

#     logger.debug(query)
#     row = await database.fetch_one(query)

#     logger.error(type(tuple(row)[0]))
#     logger.error(row.id)
#     return await row_to_model(tuple(row))

async def create_post(post: UserPostIn):
    data = post.model_dump()

    query = post_table.insert().values(data)

    logger.debug(query)
    last_record_id = await database.execute(query)
    
    return last_record_id
    
async def get_one(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)

    logger.debug(query)

    post_record = await database.fetch_one(query)
    
    if not post_record:
      raise Missing(msg=f"Post {post_id} not found")

    return post_record

async def get_all():
    query = post_table.select()

    logger.debug(query)

    post_records = await database.fetch_all(query)

    return post_records

