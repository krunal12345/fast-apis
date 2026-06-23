from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from exceptions.team_exceptions import TeamAlreadyExistsError, TeamNotFoundError
from schemas.teamSchema import PlayerSchema, TeamAddModel, TeamResponse
from services import team_service
from utils.dependencies import CurrentUser, UoWDep

router = APIRouter(tags=["teams"])


@router.get("/teams", response_model=list[TeamResponse])
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


@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team_by_id(
    _: CurrentUser,
    uow: UoWDep,
    team_id: Annotated[int, Path(..., title="Team Id", gt=0)],
):
    team = team_service.get_team_by_id(uow, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/team", status_code=status.HTTP_201_CREATED)
def add_team(_: CurrentUser, uow: UoWDep, team_data: TeamAddModel):
    try:
        team_service.add_team(uow, team_data)
    except TeamAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.put("/players/{team_id}")
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
