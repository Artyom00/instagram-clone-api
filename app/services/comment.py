from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import Comment
from app.schemas import CommentRequestBody


def create_comment(db: Session, req_body: CommentRequestBody):
    new_comment = Comment(
        text=req_body.text,
        username=req_body.username,
        post_id=req_body.post_id,
        timestamp=datetime.now()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


def get_all_comments(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()
