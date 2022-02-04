from datetime import datetime

from fastapi import status, HTTPException
from sqlalchemy import desc
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
    return db.query(Post).order_by(desc(Post.timestamp)).all()


def delete_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {post_id} not found')

    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only post creator can delete post')

    db.delete(post)
    db.commit()

    return {'message': 'Post deleted successfully'}
