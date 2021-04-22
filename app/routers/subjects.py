from datetime import datetime
from typing import List, Optional
from fastapi.param_functions import Body, Path
from pydantic import EmailStr
from fastapi import APIRouter, Query
from pydantic.main import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError
from ..models import SessionIn_Pydantic, Session_Pydantic, Session, Student, \
                        Subject, Subject_Pydantic, SubjectIn_Pydantic

router = APIRouter(
        prefix="/subjects",
        tags=["subjects"],
        responses={404: {"model": HTTPNotFoundError}}
)

@router.post("", response_model=Subject_Pydantic)
async def create_subject(subject: SubjectIn_Pydantic):
        print (subject.dict())
        subject_obj = await Subject.create(**subject.dict(exclude_unset=True))
        return await Subject_Pydantic.from_tortoise_orm(subject_obj)

@router.get("", response_model=List[Subject_Pydantic])
async def read_subjects():
        return await Subject_Pydantic.from_queryset(Subject.all())

@router.post("/{subject_id}/sessions", response_model=Session_Pydantic)
async def create_session(subject_id: int, session: SessionIn_Pydantic):
        session_obj = await Session.create(**session.dict(exclude_unset=True), subject_id=subject_id)
        return await Session_Pydantic.from_tortoise_orm(session_obj)

@router.get("/{subject_id}")
async def read_subject(subject_id: int):
        subject_obj = await Subject.get(id=subject_id)
        await subject_obj.fetch_related("students")
        await subject_obj.fetch_related("proctors")
        await subject_obj.fetch_related("sessions")

        subject_info = await Subject_Pydantic.from_tortoise_orm(subject_obj)
        students_info = [{"id": student.id, "email": student.email} for student in subject_obj.students]
        proctors_info = [{"id": proctor.id, "email": proctor.email} for proctor in subject_obj.proctors]
        sessions_info = [{"id": session.id, "email": session.scheduled} for session in subject_obj.sessions]
        return {"subject": subject_info, "students": students_info, "proctors": proctors_info, "sessions": sessions_info}


