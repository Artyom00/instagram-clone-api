from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app.db.hashing import Hash
from app.db.models import User
from app.schemas import UserRequestBody


def create_user(db: Session, req_body: UserRequestBody):
    new_user = User(
        username=req_body.username,
        email=req_body.email,
        password=Hash.encrypt(req_body.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username '{username}' not found")

    return user
