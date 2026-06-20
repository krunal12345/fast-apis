from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query
from schemas.teamSchema import TeamAddModel, Team
import services.team_service as TeamService
from exceptions.team_exceptions import TeamAlreadyExistsError

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "this is the IPL api learning project"}


@app.get("/health", description="get the health status of the api")
def health():
    return {"ok"}


@app.get("/teams", description="get all the ipl teams")
async def get_teams(
    team_Id: Annotated[
        int | None, Query(description="Filter teams by Id", gt=0, lt=14)
    ] = None,
) -> list[Team]:
    data = await TeamService.loadTeamData()
    if team_Id:
        team = TeamService.get_team_by_id(team_Id)
        return [team] if team else []
    else:
        return data


@app.get("/teams/{team_id}")
def get_team_by_id(
    team_id: Annotated[
        int, Path(..., description="pass the valid team Id", gt=0, lt=14)
    ],
) -> Team | None:
    return TeamService.get_team_by_id(team_id)


@app.post("/team", description="create a new team by passing valid team object")
async def addTeam(teamDetails: TeamAddModel):
    try:
        await TeamService.addTeam(teamDetails)
    except TeamAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)
