from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import UserDisplay, UserRequestBody
from app.services.user import create_user

router = APIRouter(prefix='/user', tags=['user'])


@router.post('', response_model=UserDisplay,
             status_code=status.HTTP_201_CREATED)
def add_user(req_body: UserRequestBody, db: Session = Depends(get_db)):
    return create_user(db, req_body)
