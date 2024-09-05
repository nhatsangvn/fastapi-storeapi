import logging

from storeapi.data import comment as data
from storeapi.errors import Missing
from storeapi.models.post import CommentIn
from storeapi.services import post as post_service

logger = logging.getLogger(__name__)

async def create_comment(comment: CommentIn):
    post_id = comment.post_id
    post = await post_service.find_post(post_id)

    if not post:
      raise Missing(msg=f"Post {post_id} not found")
    
    last_record_id = await data.create_comment(comment)
    
    input_data = comment.model_dump()
    return {**input_data, "id": last_record_id}
