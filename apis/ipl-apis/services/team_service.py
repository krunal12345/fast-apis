from schemas.teamSchema import TeamAddModel, Team
import repositories.team_repository as teamRepo
from exceptions.team_exceptions import TeamAlreadyExistsError


async def loadTeamData() -> list[Team]:
    return teamRepo.loadTeamsData()


async def addTeam(team: TeamAddModel):
    teamInDB = teamRepo.find_by_name(team.name)
    if teamInDB:
        raise TeamAlreadyExistsError(team.name)

    teamRepo.addTeam(team)


def get_team_by_id(id: int):
    return teamRepo.find_by_id(id)
