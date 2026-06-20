from schemas.teamSchema import Player, TeamAddModel, Team
import repositories.team_repository as teamRepo
from exceptions.team_exceptions import TeamAlreadyExistsError


def load_team_data() -> list[Team]:
    return teamRepo.load_teams_data()


def add_eam(team: TeamAddModel):
    teamInDB = teamRepo.find_by_name(team.name)
    if teamInDB:
        raise TeamAlreadyExistsError(team.name)

    teamRepo.addTeam(team)


def get_team_by_id(id: int):
    return teamRepo.find_by_id(id)


def add_players_by_teamid(teamId: int, players: list[Player]):
    data = load_team_data()
    team = next((t for t in data if t.id == teamId), None)
    if team:
        team.players.extend(players)

    teamRepo.save_teams_data(data)
