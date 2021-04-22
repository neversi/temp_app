from datetime import timedelta
import enum
from os import umask
from pydantic.errors import TupleLengthError
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class TimestampMixin():
        created_at = fields.DatetimeField(null=True, auto_now_add=True)
        modified_at = fields.DatetimeField(null=True, auto_now=True)

class Subject(Model):
        name = fields.CharField(max_length=255)

        students: fields.ManyToManyRelation["Student"] = fields.ManyToManyField('models.Student', related_name='subjects', through='student_subject')
        proctors: fields.ManyToManyRelation["Proctor"] = fields.ManyToManyField("models.Proctor", related_name='subjects', through='proctor_subject')
        sessions: fields.ReverseRelation["Session"]
        
class Session(Model):
        subject: fields.ForeignKeyRelation[Subject] = fields.ForeignKeyField('models.Subject', related_name="sessions")
        students: fields.ManyToManyRelation["Student"] = fields.ManyToManyField('models.Student', relatied_name='sessions', through='student_session')
        proctors: fields.ManyToManyRelation["Proctor"] = fields.ManyToManyField('models.Proctor', related_name="sessions", through='proctor_session')
        scheduled = fields.DatetimeField(null=True, auto_now_add=True)
        reports: fields.ReverseRelation["Report"]
        
class Student(Model):
        email = fields.CharField(max_length=255, unique=True)
        sessions: fields.ManyToManyRelation[Session]
        password = fields.CharField(max_length=255)
        on_exam = fields.BooleanField(default=False)
        subjects: fields.ManyToManyRelation[Subject]
        reports: fields.ReverseRelation["Report"]

class Proctor(Model):
        email = fields.CharField(max_length=255, unique=True)
        password = fields.CharField(max_length=255)
        subjects: fields.ManyToManyRelation[Subject]
        sessions: fields.ManyToManyRelation[Session]

        class PydanticMeta:
                email: EmailStr

class Report(Model):
        time_duration = fields.TimeDeltaField(default=timedelta(seconds=0))
        video_web = fields.TextField()
        video_screen = fields.TextField()
        trust_point = fields.IntField(default=100)

        session: fields.ForeignKeyRelation[Session] = fields.ForeignKeyField('models.Session', related_name='reports')
        student: fields.ForeignKeyRelation[Student] = fields.ForeignKeyField('models.Student', related_name='reports')
        warnings: fields.ReverseRelation["WarningCV"]

class WarningEnum(enum.Enum):
        Absence = 1
        More    = 2
        XY      = 3
        XZ      = 4
        YZ      = 5

class WarningCV(TimestampMixin, Model):
        frame = fields.TextField(null=True)
        duration = fields.TimeDeltaField()
        report: fields.ForeignKeyRelation[Report] = fields.ForeignKeyField('models.Report', related_name='warnings')
        type_warning = fields.SmallIntField(default=1)

        class Meta:
                table = 'warning'

        
Student_Pydantic = pydantic_model_creator(Student, name="Student", exclude=('password',))
StudentIn_Pydantic = pydantic_model_creator(Student, name="StudentIn")

Subject_Pydantic = pydantic_model_creator(Subject, name="Subject")
SubjectIn_Pydantic = pydantic_model_creator(Subject, name="SubjectIn")

Proctor_Pydantic = pydantic_model_creator(Proctor, name="Proctor", exclude=('password',))
ProctorIn_Pydantic = pydantic_model_creator(Proctor, name="ProctorIn", exclude_readonly=True)

Session_Pydantic = pydantic_model_creator(Session, name="Sesion")
SessionIn_Pydantic = pydantic_model_creator(Session, name="SessionIn")

Report_Pydantic = pydantic_model_creator(Report, name="Report")
Warning_Pydantic = pydantic_model_creator(WarningCV, name="Warning")

class UserCreate(BaseModel):
        email: EmailStr
        password: str