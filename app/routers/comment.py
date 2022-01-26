from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.schemas import CommentRequestBody, UserAuth
from app.services.comment import create_comment, get_all_comments

router = APIRouter(prefix='/comment', tags=['comment'])


@router.post('')
def add_comment(req_body: CommentRequestBody, db: Session = Depends(get_db),
                current_user: UserAuth = Depends(get_current_user)):
    return create_comment(db, req_body)


@router.get('/all/{post_id}')
def get_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    return get_all_comments(db, post_id)
