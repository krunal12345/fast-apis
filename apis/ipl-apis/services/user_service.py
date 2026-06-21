from exceptions.user_exceptions import UserAlreadyExistsError
from schemas.user_models import UserInput, User
import repositories.user_details as user_repo
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(entered_pass: str, actual_pass: str) -> bool:
    return bcrypt.checkpw(entered_pass.encode("utf-8"), actual_pass.encode("utf-8"))


def get_last_user_id() -> int:
    return user_repo.get_last_user_id()


def get_users() -> list[User]:
    return user_repo.load_users()


def add_user(user: UserInput):

    user_db = user_repo.get_user_by_email(user.email)
    if user_db:
        raise UserAlreadyExistsError(user.email)

    user_add = User(
        **user.model_dump(exclude={"id", "password"}),
        id=get_last_user_id() + 1,
        password_hash=hash_password(user.password),
    )
    user_repo.add_user(user_add)
