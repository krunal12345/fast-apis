from schemas.teamSchema import TeamAddModel
import repositories.team_repository as teamRepo
from exceptions.team_exceptions import TeamAlreadyExistsError


async def loadTeamData():
    return teamRepo.loadTeamsData()


async def addTeam(team: TeamAddModel):
    teamInDB = teamRepo.find_by_name(team.name)
    if teamInDB:
        raise TeamAlreadyExistsError(f"Team with {team.name} already exists")

    teamRepo.addTeam(team)
