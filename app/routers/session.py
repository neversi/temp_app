from app.routers.subjects import create_session
from typing import List, Optional

from fastapi.responses import FileResponse
from fastapi import APIRouter, BackgroundTasks
from pydantic.main import BaseModel
from starlette.responses import StreamingResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from ..models import Report_Pydantic, Session, Report, Student, Subject, WarningCV, WarningEnum, Warning_Pydantic
from ..helpers.xlsx import _create_session_xlsx 
from tortoise.exceptions import DoesNotExist

router = APIRouter(
        prefix="/session",
        tags=["sessions"],
        responses={404: {"model": HTTPNotFoundError}}
)

