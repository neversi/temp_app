from typing import List, Optional
from fastapi.param_functions import Body, Path
from pydantic import EmailStr
from fastapi import APIRouter, Query
from tortoise.contrib.fastapi import HTTPNotFoundError
from ..models import Student_Pydantic, StudentIn_Pydantic, Student, \
                        Subject, Subject_Pydantic, UserCreate

from ..redis import redis_cache

                        
router = APIRouter(
        prefix="/students",
        tags=["students"],
        responses={404: {"model": HTTPNotFoundError}}
)

@router.on_event('startup')
async def starup_event():
    await redis_cache.init_cache()


@router.on_event('shutdown')
async def shutdown_event():
    redis_cache.close()
    await redis_cache.wait_closed()

@router.get("/score/alina/{score}")
async def set_score(score: int):
        redis_cache.redis_cache.set("alina", str(score))

@router.get("", response_model=List[Student_Pydantic])
async def read_students():
        return await Student_Pydantic.from_queryset(Student.all())

class StudentCreate(UserCreate):
        on_exam: Optional[bool] = False

@router.post("", response_model=Student_Pydantic)
async def create_student(student: StudentCreate):
        student_obj = await Student.create(**student.dict(exclude_unset=True))
        return await Student_Pydantic.from_tortoise_orm(student_obj)

@router.get("/{student_id}", response_model=Student_Pydantic)
async def read_student(student_id: int):
        return await Student_Pydantic.from_queryset_single(Student.get(id=student_id))

@router.get("/{student_id}/subjects", response_model=List[Subject_Pydantic])
async def read_student_subjects(student_id: int):
        return await Subject_Pydantic.from_queryset(Subject.filter(students__id=student_id))

@router.post("/{student_id}/subjects/{subject_id}", response_model=List[Subject_Pydantic])
async def enroll_student(student_id: int, subject_id: int):
        subject_obj = await Subject.get_or_none(id=subject_id)
        student_obj = await Student.get(id=student_id)
        await student_obj.subjects.add(subject_obj)
        
        return await Subject_Pydantic.from_queryset(Subject.filter(students__id=student_id))


        

