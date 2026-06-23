from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordRequestForm

from exceptions.team_exceptions import TeamAlreadyExistsError, TeamNotFoundError
from exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from models.user_models import Tokens, UserInput
from schemas.teamSchema import PlayerSchema, TeamAddModel, TeamResponse
from schemas.user_models import UserBase
import services.team_service as team_service
import services.user_service as user_service
from utils.dependencies import CurrentUser, UoWDep
from utils.user_utils import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "this is the IPL api learning project"}


@app.get("/health")
def health():
    return {"ok"}


# --- Teams ---


@app.get("/teams", response_model=list[TeamResponse])
def get_teams(
    _: CurrentUser,
    uow: UoWDep,
    team_id: Annotated[
        int | None,
        Query(description="Filter teams by Id", gt=0),
    ] = None,
):
    if team_id:
        team = team_service.get_team_by_id(uow, team_id)
        return [team] if team else []
    return team_service.get_all_teams(uow)


@app.get("/teams/{team_id}", response_model=TeamResponse)
def get_team_by_id(
    _: CurrentUser,
    uow: UoWDep,
    team_id: Annotated[int, Path(..., title="Team Id", gt=0)],
):
    team = team_service.get_team_by_id(uow, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.post("/team", status_code=status.HTTP_201_CREATED)
def add_team(_: CurrentUser, uow: UoWDep, team_data: TeamAddModel):
    try:
        team_service.add_team(uow, team_data)
    except TeamAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


@app.put("/players/{team_id}")
def add_players(
    _: CurrentUser,
    uow: UoWDep,
    team_id: Annotated[int, Path(..., gt=0)],
    players: Annotated[list[PlayerSchema], Body(embed=True)],
):
    try:
        team_service.add_players_to_team(uow, team_id, players)
    except TeamNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


# --- Users ---


@app.get("/users", response_model=list[UserBase], tags=["Users"])
def get_users(_: CurrentUser, uow: UoWDep):
    return user_service.get_users(uow)


@app.post("/user", status_code=status.HTTP_201_CREATED, tags=["Users"])
def add_user(
    _: CurrentUser,
    uow: UoWDep,
    user_input: Annotated[UserInput, Body(description="User to add")],
):
    try:
        user_service.add_user(uow, user_input)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


# --- Auth ---


@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(
    uow: UoWDep,
    user_input: Annotated[UserInput, Body(description="Sign up for a new account")],
):
    try:
        user_service.add_user(uow, user_input)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


@app.post("/token", response_model=Tokens, tags=["Auth"])
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], uow: UoWDep):
    try:
        return user_service.login(uow, form)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
