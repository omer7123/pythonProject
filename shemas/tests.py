from pydantic import BaseModel
from shemas.users import Token, UserInfo


class Answers(BaseModel):
    id: str
    right: bool
    title: str

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: str
    question: str
    right_answer: int
    passed: int
    passed_correctly: int
    answers: list[Answers]

    class Config:
        orm_mode = True


class Test(BaseModel):
    id: str
    title: str
    access: bool
    id_authors: str
    username: str
    passed: int
    passed_correctly: int
    questions: list[Question]


    class Config:
        orm_mode = True


class TestInfo(BaseModel):
    id: str
    title: str
    access: bool
    id_authors: str
    username: str
    passed: int
    passed_correctly: int

    class Config:
        orm_mode = True


class CreateAnswers(BaseModel):
    title: str
    right: bool

    class Config:
        orm_mode = True


class CreateQuestion(BaseModel):
    question: str
    right_answer: int
    answers: list[CreateAnswers]

    class Config:
        orm_mode = True


class CreateTest(BaseModel):
    title: str
    user: Token
    questions: list[CreateQuestion]
    id_authors: str
    username: str

    class Config:
        orm_mode = True


class PlayAnswer(BaseModel):
    id: str
    right: bool

    class Config:
        orm_mode = True


class PlayQuestion(BaseModel):
    id: str
    answers: list[PlayAnswer]

    class Config:
        orm_mode = True


class PlayTest(BaseModel):
    id: str
    user: UserInfo
    questions: list[PlayQuestion]

    class Config:
        orm_mode = True


class ResultTest(BaseModel):
    id: str
    questions: list[CreateQuestion]
    result: str

    class Config:
        orm_mode = True
