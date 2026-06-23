from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from models.team_models import Team, Player
from repositories.abstract_repository import AbstractTeamRepository


class TeamRepository(AbstractTeamRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Team]:
        return list(
            self.session.exec(select(Team).options(selectinload(Team.players))).all()
        )

    def get_by_id(self, id: int) -> Team | None:
        return self.session.exec(
            select(Team).where(Team.id == id).options(selectinload(Team.players))
        ).first()

    def get_by_name(self, name: str) -> Team | None:
        return self.session.exec(select(Team).where(Team.name == name)).first()

    def add(self, team: Team) -> Team:
        self.session.add(team)
        return team

    def add_players(self, team: Team, players: list[Player]) -> None:
        for player in players:
            player.team_id = team.id
            self.session.add(player)
