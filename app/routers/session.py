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

class CreateSessionIn(BaseModel):
        user_id: str
        user_name: str
        user_role: str
        course_id: str
        resource_id: str
        user_full_name: str
        course_title: str
        resource_title: str
        exam_url: str
        screen_session_id: Optional[int] = None
        webcam_session_id: Optional[int] = None


@router.post("")
async def create_moodle_session(create_sesion_in: CreateSessionIn):
        session_obj = await Session.get_or_none(id=int(create_sesion_in.resource_id))
        (subject_obj, exists) = await Subject.get_or_create(id=int(create_sesion_in.course_id), name=create_sesion_in.course_title)
        if session_obj is None:
                session_obj = await Session.create(subject_id=int(create_sesion_in.course_id), id=int(create_sesion_in.resource_id))
        (student_obj, exists) = await Student.update_or_create(id=int(create_sesion_in.user_id), email=create_sesion_in.user_full_name, password="null")
        await session_obj.fetch_related("students")
        await session_obj.students.add(student_obj)
        await subject_obj.fetch_related("students")
        await subject_obj.students.add(student_obj)
        await Report.create(session_id = int(create_sesion_in.resource_id), student_id = int(create_sesion_in.user_id), video_web = str(create_sesion_in.webcam_session_id), video_screen = str(create_sesion_in.screen_session_id))
        return {"message" : "Session started"}