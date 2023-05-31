import uuid
import pydantic
from pydantic import BaseModel


class Creds(pydantic.BaseModel):
    username: str
    password: str
    password1: str


class User(pydantic.BaseModel):
    id: str
    username: str
    password: str
    token: str
    passed_tests: list[str]


class UserUpdate(BaseModel):
    id: str
    token: str
    username: str


class Token(BaseModel):
    token: str


class UserInfo(BaseModel):
    id: str
    token: str
