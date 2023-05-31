import uuid

from fastapi import APIRouter, Query
from shemas.users import User, UserUpdate, Creds
from services.users import user_service

router = APIRouter()


@router.post(
    "/users/register",
    response_model=UserUpdate,
)
def add_user(user: Creds):
    return user_service.add_user(user)


@router.post(
    "/users/auth",
    response_model=UserUpdate,
)
def auth_user(username: str = Query(...), password: str = Query(...)):
    return user_service.auth_user(username, password)

