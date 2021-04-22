from typing import List, Optional
from fastapi.param_functions import Body, Path
from fastapi.exceptions import HTTPException
from pydantic import EmailStr, BaseModel
from fastapi import APIRouter, Query
from starlette.background import BackgroundTasks
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.query_utils import Q
from ..models import Proctor_Pydantic, ProctorIn_Pydantic, Proctor, Session, Session_Pydantic, \
                        Subject, Subject_Pydantic, SubjectIn_Pydantic, UserCreate
from datetime import datetime

router = APIRouter(
        prefix="/proctors",
        tags=["proctors"],
        responses={404: {"model": HTTPNotFoundError}}
)

@router.get("", response_model=List[Proctor_Pydantic])
async def read_proctors():
        return await Proctor_Pydantic.from_queryset(Proctor.all())

@router.post("", response_model=Proctor_Pydantic)
async def create_proctor(proctor: UserCreate):
        proctor_obj = await Proctor.create(**proctor.dict(exclude_unset=True))
        return await Proctor_Pydantic.from_tortoise_orm(proctor_obj)

@router.get("/{proctor_id}", response_model=Proctor_Pydantic)
async def read_proctor(proctor_id: int):
        return Proctor_Pydantic.from_queryset_single(Proctor.get(id=proctor_id))

@router.get("/{proctor_id}/subjects", response_model=List[Subject_Pydantic])
async def read_proctor_subjects(proctor_id: int):
        return await Subject_Pydantic.from_queryset(Subject.filter(proctors__id=proctor_id))

@router.post("/{proctor_id}/subjects/{subject_id}", response_model=List[Subject_Pydantic])
async def enroll_proctor(proctor_id: int, subject_id: int):
        subject_obj = await Subject.get_or_none(id=subject_id)
        proctor_obj = await Proctor.get(id=proctor_id)
        await proctor_obj.subjects.add(subject_obj)
        
        return await Subject_Pydantic.from_queryset(Subject.filter(proctors__id=proctor_id))

@router.post("/{proctor_id}/sessions/{session_id}", response_model=Session_Pydantic)
async def enroll_session(proctor_id: int, session_id: int):
        proctor_obj = await Proctor.get(id=proctor_id)
        session_obj = await Session.get(id=session_id)
        await session_obj.fetch_related("subject__proctors")

        if proctor_obj not in session_obj.subject.proctors:
                raise HTTPException(status_code=401, detail="Not allowed to enroll")
        
        await proctor_obj.sessions.add(session_obj)
        return await Session_Pydantic.from_tortoise_orm(session_obj)


@router.get("/{proctor_id}/sessions", response_model=List[Session_Pydantic])
async def read_sessions(proctor_id: int):
        proctor_obj = await Proctor.get(id=proctor_id)
        return await Session_Pydantic.from_queryset(proctor_obj.sessions.all())
