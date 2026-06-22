from typing import Annotated
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, status
from exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from fastapi.security import OAuth2PasswordRequestForm
from schemas.teamSchema import Player, TeamAddModel, Team
from schemas.user_models import Tokens, UserBase, UserInput
import services.team_service as TeamService
import services.user_service as user_service
from exceptions.team_exceptions import TeamAlreadyExistsError
from utils.user_utils import create_db_and_tables, get_current_user

app = FastAPI()

user = Annotated[UserBase, Depends(get_current_user)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "this is the IPL api learning project"}


@app.get("/health", description="get the health status of the api")
def health():
    return {"ok"}


@app.get(
    "/teams",
    description="get all the ipl teams",
    response_model=list[Team],
    response_model_exclude_unset=True,
)
async def get_teams(
    user: user,
    team_Id: Annotated[
        int | None,
        Query(description="Filter teams by Id", gt=0, lt=14),
    ] = None,
) -> list[Team]:
    data = TeamService.load_team_data()
    if team_Id:
        team = TeamService.get_team_by_id(team_Id)
        return [team] if team else []
    else:
        return data


@app.get("/teams/{team_id}")
def get_team_by_id(
    user: user,
    team_id: Annotated[
        int,
        Path(
            ...,
            title="Id of the team to Get",
            description="pass the valid team Id",
            gt=0,
            lt=14,
        ),
    ],
) -> Team | None:
    return TeamService.get_team_by_id(team_id)


@app.post("/team", description="create a new team by passing valid team object")
def add_team(teamDetails: TeamAddModel, user: user):
    try:
        TeamService.add_eam(teamDetails)
    except TeamAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


@app.put("/players/{team_id}", description="add a players to the team By Team Id")
def add_players(
    user: user,
    team_id: Annotated[int, Path(..., gt=0, lt=14)],
    players: Annotated[list[Player], Body(embed=True)],
):
    team = TeamService.get_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team with given Id found")
    else:
        TeamService.add_players_by_teamid(team_id, players)


@app.get("/users", response_model=list[UserBase], tags=["Users"])
def get_users(user: user):
    return user_service.get_users()


@app.post("/user", tags=["Users"])
def add_user(
    user: user,
    userItem: Annotated[UserInput, Body(description="user model to add in the system")],
):
    try:
        user_service.add_user(userItem)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


@app.post("/token", response_model=Tokens, tags=["Auth"])
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        return user_service.login(form)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
