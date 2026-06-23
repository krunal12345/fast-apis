from exceptions.team_exceptions import TeamAlreadyExistsError, TeamNotFoundError
from models.team_models import Team, Player
from schemas.teamSchema import TeamAddModel, PlayerSchema
from utils.unit_of_work import AbstractUnitOfWork


def get_all_teams(uow: AbstractUnitOfWork) -> list[Team]:
    return uow.teams.get_all()


def get_team_by_id(uow: AbstractUnitOfWork, team_id: int) -> Team | None:
    return uow.teams.get_by_id(team_id)


def add_team(uow: AbstractUnitOfWork, team_data: TeamAddModel) -> None:
    existing = uow.teams.get_by_name(team_data.name)
    if existing:
        raise TeamAlreadyExistsError(team_data.name)

    new_team = Team(
        name=team_data.name,
        short_name=team_data.short_name,
        home_city=team_data.home_city,
        home_ground_name=team_data.home_ground_name,
        total_trophies=team_data.total_trophies,
    )
    uow.teams.add(new_team)


def add_players_to_team(
    uow: AbstractUnitOfWork, team_id: int, players_data: list[PlayerSchema]
) -> None:
    team = uow.teams.get_by_id(team_id)
    if not team:
        raise TeamNotFoundError(team_id)

    players = [
        Player(
            name=p.name,
            jersey_number=p.jersey_number,
            total_runs=p.total_runs,
            team_id=team_id,
        )
        for p in players_data
    ]
    uow.teams.add_players(team, players)
