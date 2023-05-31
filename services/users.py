from uuid import uuid4

from fastapi import HTTPException, Query

import sql.db.db as db
from shemas.users import User, Creds, UserUpdate


class UserService:

    def add_user(self, creds: Creds) -> UserUpdate:
        if creds.password == creds.password1:
            token = "token_" + uuid4().__str__()
            id = uuid4().__str__()
            user = User(
                id=id,
                username=creds.username,
                password=creds.password,
                token=token,
                passed_tests=[]
            )
            return db.add_user(user)
        raise HTTPException(status_code=400, detail="Введенные Вами пароли не совпдают")

    def auth_user(self, username: str = Query(...), password: str = Query(...)) -> UserUpdate:
        return db.auth_user(username, password)


user_service: UserService = UserService()
