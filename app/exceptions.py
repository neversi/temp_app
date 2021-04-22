from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import IntegrityError
from fastapi import FastAPI, Request

class UserNotExist(Exception):
        def __init__(self, email: str):
                self.email = email

def add_exceptions(app: FastAPI):
        @app.exception_handler(UserNotExist)
        async def user_not_exist(request: Request, exc: UserNotExist):
                return JSONResponse(
                        status_code=404,
                        content={"message": f"User {exc.email} does not exist"}
                )