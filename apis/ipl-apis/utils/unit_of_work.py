from abc import ABC, abstractmethod

from sqlmodel import Session

from utils.user_utils import engine
from repositories.abstract_repository import AbstractUserRepository, AbstractTeamRepository
from repositories.user_details import UserRepository
from repositories.team_repository import TeamRepository


class AbstractUnitOfWork(ABC):
    """
    Contract every UoW implementation must satisfy.
    Services depend on this, never on the concrete class — so tests can
    swap in a FakeUnitOfWork with zero real DB calls.
    """

    users: AbstractUserRepository
    teams: AbstractTeamRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """
    Production implementation — one SQLAlchemy Session per UoW instance.

    Two usage modes:
      1. Context manager (scripts / tests):
            with SqlAlchemyUnitOfWork() as uow:
                uow.users.add(user)

      2. FastAPI dependency (see utils/dependencies.py):
            uow = SqlAlchemyUnitOfWork()
            uow.session = Session(engine)   # set by get_uow()
    """

    session: Session

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = Session(engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    @property
    def users(self) -> UserRepository:
        return UserRepository(self.session)

    @property
    def teams(self) -> TeamRepository:
        return TeamRepository(self.session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
