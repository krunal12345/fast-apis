from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm

from exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from models.user_models import User, UserInput, Tokens
from utils.unit_of_work import AbstractUnitOfWork
import bcrypt
import jwt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(entered_pass: str, actual_pass: str) -> bool:
    return bcrypt.checkpw(entered_pass.encode("utf-8"), actual_pass.encode("utf-8"))


def get_users(uow: AbstractUnitOfWork) -> list[User]:
    return uow.users.get_all()


def add_user(uow: AbstractUnitOfWork, user_input: UserInput) -> None:
    existing = uow.users.get_by_email(user_input.email)
    if existing:
        raise UserAlreadyExistsError(user_input.email)

    new_user = User(
        name=user_input.name,
        email=user_input.email,
        password_hash=hash_password(user_input.password),
    )
    uow.users.add(new_user)


def login(uow: AbstractUnitOfWork, form: OAuth2PasswordRequestForm) -> Tokens:
    user_db = uow.users.get_by_email(form.username)

    if not user_db:
        raise InvalidCredentialsError()

    if not verify_password(form.password, user_db.password_hash):
        raise InvalidCredentialsError()

    token = jwt.encode(
        {
            "id": user_db.id,
            "sub": user_db.email,
            "username": user_db.name,
            "exp": datetime.now() + timedelta(minutes=10),
        },
        "JustRandomJWTLearningString",
        "HS256",
    )

    return Tokens(access_token=token, token_type="bearer")
