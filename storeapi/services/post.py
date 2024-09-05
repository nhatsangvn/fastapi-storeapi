import logging

logger = logging.getLogger(__name__)


from storeapi.data import comment as data_comment  # noqa: E402
from storeapi.data import post as data  # noqa: E402
from storeapi.models.post import UserPost, UserPostIn  # noqa: E402


async def create_post(post: UserPostIn):
    logger.info("Creating post")

    last_record_id = await data.create_post(post)

    input_data = post.model_dump()
    return {**input_data, "id": last_record_id}

async def find_post(post_id: int) -> int:
    logger.info(f"Finding post with id {post_id}")

    post_record = await data.get_one(post_id)

    return post_record

async def get_all_post() -> list[UserPost]:
    all_record = await data.get_all()

    return all_record



async def find_post_comment(post_id):
    await find_post(post_id)

    return await data_comment.get_comment_on_post(post_id)

    
