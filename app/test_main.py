from fastapi.params import Header
from fastapi.testclient import TestClient
from pypika.terms import RangeCriterion
from starlette import responses
import pytest
from .main import app
from tortoise.contrib.fastapi import register_tortoise

client = TestClient(app)

# def test_create_student():
#         response = client.post(
#                 "/api/v1/students",
#                 json={
#                         "email": "Student " + str(1),
#                         "password": "student" + str(1),
#                         "on_exam": True
#                 }
#         )

        # assert response.status_code == 200

# @pytest.fixture(scope="session", autouse=True)

@pytest.fixture(scope="function")
def init_db():
    register_tortoise(
        app,
        db_url="postgres://postgres:qwerty123@localhost:5432/test_db",
        modules={'models': ['app.models']},
        generate_schemas=True,
        add_exception_handlers=True,
)

def test_create_subject(init_db):
        response = client.post(
                "/api/v1/subjects",
                headers={"Content-Type": "application/json"},
                json= {
                        "id": 11,
                        "name": "Subject 1"
                }
        )
        assert response.status_code == 200

