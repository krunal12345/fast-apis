from fastapi import FastAPI
from schemas.teamSchema import TeamAddModel, Team
import services.team_service as TeamService

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "this is the IPL api learning project"}


@app.get("/health")
def health():
    return {"ok"}


@app.get("/teams")
async def get_teams() -> list[Team]:
    return await TeamService.loadTeamData()


@app.post("/team")
async def addTeam(teamDetails: TeamAddModel):
    await TeamService.addTeam(teamDetails)
