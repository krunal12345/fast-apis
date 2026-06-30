from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Security, status

from exceptions.user_exceptions import UserAlreadyExistsError
from models.user_models import UserBase, UserInput
from services import user_service
from utils.dependencies import CurrentUser, UoWDep
from utils.user_utils import get_current_user

router = APIRouter(
    tags=["Users"], dependencies=[Security(get_current_user, scopes=["users"])]
)


@router.get(
    "/users",
    response_model=list[UserBase],
)
def get_users(_: CurrentUser, uow: UoWDep):
    return user_service.get_users(uow)


@router.post("/user", status_code=status.HTTP_201_CREATED)
def add_user(
    _: CurrentUser,
    uow: UoWDep,
    user_input: Annotated[UserInput, Body(description="User to add")],
):
    try:
        user_service.add_user(uow, user_input)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)
