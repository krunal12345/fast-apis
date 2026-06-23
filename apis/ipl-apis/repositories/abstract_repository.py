from abc import ABC, abstractmethod

from models.user_models import User
from models.team_models import Team, Player


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[User]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def add(self, user: User) -> User: ...


class AbstractTeamRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Team]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> Team | None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Team | None: ...

    @abstractmethod
    def add(self, team: Team) -> Team: ...

    @abstractmethod
    def add_players(self, team: Team, players: list[Player]) -> None: ...
