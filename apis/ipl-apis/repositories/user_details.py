from sqlmodel import Session, select

from models.user_models import User
from repositories.abstract_repository import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[User]:
        return list(self.session.exec(select(User)).all())

    def get_by_id(self, id: int) -> User | None:
        return self.session.get(User, id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.exec(select(User).where(User.email == email)).first()

    def add(self, user: User) -> User:
        self.session.add(user)
        return user
