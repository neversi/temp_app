from fastapi.applications import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic.networks import RedisDsn
from starlette.requests import Request
from starlette.responses import JSONResponse
from .routers import students, subjects, proctors, sessions,session
from .config import Config
from tortoise.contrib.fastapi import register_tortoise
from .ws import socket_app
from .exceptions import UserNotExist, add_exceptions
from .redis import redis_cache

app = FastAPI()


origins = [
        "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(proctors.router)
app.include_router(sessions.router)
app.include_router(session.router)

app.mount('/ws', socket_app)

register_tortoise(
        app,
        db_url=Config.SQLALCHEMY_DATABASE_URL,
        modules={'models': ['app.models']},
        generate_schemas=False,
        add_exception_handlers=True,
)


@app.on_event('startup')
async def starup_event():
    await redis_cache.init_cache()


@app.on_event('shutdown')
async def shutdown_event():
    redis_cache.close()
    await redis_cache.wait_closed()


