from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import user
from app.routers import post

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)

app.mount('/images', StaticFiles(directory='images'), name='images')
