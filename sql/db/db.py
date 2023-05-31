import json
import uuid

from fastapi import HTTPException, Query
from sqlalchemy import create_engine, Column, String, Integer, update, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from shemas.users import User, Creds, UserUpdate

Base = declarative_base()


class TableUser(Base):
    __tablename__ = "users"
    id = Column("id", String, primary_key=True)
    username = Column("username", String)
    password = Column("password", String)
    token = Column("token", String)
    passed_tests = Column("passed_tests", JSON)


engine = create_engine("sqlite:///db/users.db", echo=False)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def user_to_table_user(user: User) -> TableUser:
    return TableUser(
        id=user.id,
        username=user.username,
        password=user.password,
        token=user.token,
        passed_tests=json.dumps(user.passed_tests)
    )


def table_to_user(user: TableUser) -> User:
    return User(
        id=user.id,
        username=user.username,
        password=user.password,
        token=user.token
    )


def add_user(user: User) -> UserUpdate:
    us = session.query(TableUser).filter_by(username=user.username).first()
    if not us:
        table_user = user_to_table_user(user)
        session.add(table_user)
        session.commit()
        return UserUpdate(
            id=user.id,
            token=user.token,
            username=user.username
        )
    raise HTTPException(status_code=400, detail="A user with the same name already exists")


def auth_user(username: str = Query(...), password: str = Query(...)) -> UserUpdate:
    us = session.query(TableUser).filter_by(username=username).first()
    print("fdfd",json.loads(us.passed_tests))
    if us and us.password == password:
        token = "token_" + uuid.uuid4().__str__()
        stmt = update(TableUser).where(TableUser.id == us.id).values(token=token)
        session.execute(stmt)
        session.commit()
        return UserUpdate(
            id=us.id,
            token=token,
            username=us.username
        )
    raise HTTPException(status_code=400, detail="Error: wrong login or password")


def token_verification(token, id_authors) -> bool:
    user = session.query(TableUser).filter_by(id=id_authors).first()
    if user:
        if user.token == token:
            return True
        raise HTTPException(status_code=400, detail="Token is invalid")
    raise HTTPException(status_code=400, detail="User with this id not found")


def update_passed(id_user: str, id_test: str):
    user = session.query(TableUser).filter_by(id=id_user).first()
    passed_tests = json.loads(user.passed_tests)
    passed_tests.append(id_test)
    print("id_test: fjldskfhhhhhhhhhhhhhhhh",passed_tests)
    passed_json=json.dumps(passed_tests)
    user.passed_tests=passed_json
    session.commit()


def get_correctly_ids_tests(id):
    user = session.query(TableUser).filter_by(id=id).first()
    passed_tests = json.loads(user.passed_tests)
    return passed_tests