from typing import List

from fastapi.responses import FileResponse
from fastapi import APIRouter, BackgroundTasks
from pydantic.main import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError
from ..models import Report_Pydantic, Session, Report, WarningCV, WarningEnum, Warning_Pydantic
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

