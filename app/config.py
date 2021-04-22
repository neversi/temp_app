from dotenv import load_dotenv
from os import getenv
from os import path

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class Config(object):
        SQLALCHEMY_DATABASE_URL: str = getenv("SQLALCHEMY_DATABASE_URL") or "postgresql://proctoring:dbpassword@localhost:5432/narxoz"
        ACCESS_SECRET_KEY: str = getenv("ACCESS_SECRET_KEY") or "secretkey"
        REFRESH_SECRET_KEY: str = getenv("REFRESH_SECRET_KEY") or 'secretkey'
        STUDENT_SERVICE_URL = getenv("STUDENT_SERVICE_URL")
        PROCTOR_SERVICE_URL = getenv("PROCTOR_SERVICE_URL")
        REDIS_URL=getenv("REDIS_URL")
        REDIS_ADDR=getenv("REDIS_ADDR")
        REDIS_PORT=getenv("REDIS_PORT")


TORTOISE_ORM = {
                "connections": {"default": Config.SQLALCHEMY_DATABASE_URL},
                "apps": {
                        "models": {
                                "models": ["app.models", "aerich.models"],
                                "default_connection": "default",
                        },
                },
        }