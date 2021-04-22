from typing import List, Optional

from fastapi.responses import FileResponse
from fastapi import APIRouter, BackgroundTasks
from pydantic.main import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError
from ..models import Report_Pydantic, Session, Report, WarningCV, WarningEnum, Warning_Pydantic, Subject, Student
from ..helpers.xlsx import _create_session_xlsx 

router = APIRouter(
        prefix="/sessions",
        tags=["sessions"],
        responses={404: {"model": HTTPNotFoundError}}
)

@router.get("/xlsx/{session_id}")
async def upload_xlsx(session_id: int):
        # background_tasks.add_task(_create_session_xlsx, session_id)
        file_name = await _create_session_xlsx(session_id)
        return FileResponse(file_name)

class ReportFull(Report_Pydantic):
        student_id: int

class ReportWarnings(ReportFull):
        student_id: int
        warnings: List[Warning_Pydantic]

@router.get("/{session_id}/reports", response_model=List[ReportWarnings])
async def read_reports(session_id: int):
        session_obj = await Session.get(id=session_id)
        await session_obj.fetch_related("reports__warnings")
        return await ReportWarnings.from_queryset(session_obj.reports.all())


@router.post("/{session_id}/reports", response_model=Report_Pydantic, deprecated=True)
async def create_report(session_id: int, report: ReportFull):
        report_obj = await Report.create(**report.dict(exclude_unset=True), session_id=session_id)
        return await Report_Pydantic.from_tortoise_orm(report_obj)

@router.post("/{session_id}/reports/{report_id}", response_model=Warning_Pydantic, deprecated=True)
async def create_warning(session_id: int, report_id: int, warning: Warning_Pydantic): #TEST!!!
        warning_obj = await WarningCV.create(**warning.dict(exclude={'type_warning'}), report_id=report_id)
        return await Warning_Pydantic.from_tortoise_orm(warning_obj)

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


@router.post("/create")
async def create_moodle_session(create_sesion_in: CreateSessionIn):
        # session_obj = await Session.get_or_none(id=int(create_sesion_in.resource_id))
        subject_obj = await Subject.create(id=int(create_sesion_in.course_id), name=create_sesion_in.course_title)
        # if session_obj is None:
        await Session.create(subject_id=int(create_sesion_in.course_id), id=int(create_sesion_in.resource_id))
        await Student.create(id=int(create_sesion_in.user_id), email=create_sesion_in.user_full_name, password="null")
        await Report.create(session_id = int(create_sesion_in.resource_id), student_id = int(create_sesion_in.user_id), video_web = str(create_sesion_in.webcam_session_id), video_screen = str(create_sesion_in.screen_session_id))
        return {"message" : "Session started"}