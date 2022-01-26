from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import user, post, authentication, comment

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(comment.router)

app.mount('/images', StaticFiles(directory='images'), name='images')
