import shutil
import string
import random
from typing import List

from fastapi import status, APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.schemas import PostDisplay, PostRequestBody, UserAuth
from app.services.post import create_post, get_posts_list, delete_post

router = APIRouter(prefix='/post', tags=['post'])
image_url_types = ['absolute', 'relative']


@router.post('', response_model=PostDisplay,
             status_code=status.HTTP_201_CREATED)
def add_post(req_body: PostRequestBody, db: Session = Depends(get_db),
             current_user: UserAuth = Depends(get_current_user)):
    if req_body.image_url_type not in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can only take "
                                   "values 'absolute' or 'relative'")
    return create_post(db, req_body)


@router.get('', response_model=List[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return get_posts_list(db)


@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    rand_str = ''.join(random.choice(string.ascii_letters) for _ in range(6))
    postfix = f'_{rand_str}.'
    path = f"images/{postfix.join(image.filename.rsplit('.', 1))}"

    with open(path, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.delete('/delete/{id_}')
def remove_post(id_: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return delete_post(db, id_, current_user.id)
