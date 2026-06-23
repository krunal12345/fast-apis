from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from models.user_models import Tokens, UserInput
from services import user_service
from utils.dependencies import UoWDep

router = APIRouter(tags=["auth"])


# --- Auth ---


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    uow: UoWDep,
    user_input: Annotated[UserInput, Body(description="Sign up for a new account")],
):
    try:
        user_service.add_user(uow, user_input)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.post("/token", response_model=Tokens)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], uow: UoWDep):
    try:
        return user_service.login(uow, form)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
