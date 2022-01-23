from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Post
from app.schemas import PostRequestBody


def create_post(db: Session, req_body: PostRequestBody):
    new_post = Post(
        image_url=req_body.image_url,
        image_url_type=req_body.image_url_type,
        caption=req_body.caption,
        timestamp=datetime.now(),
        user_id=req_body.creator_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def get_posts_list(db: Session):
    return db.query(Post).all()
