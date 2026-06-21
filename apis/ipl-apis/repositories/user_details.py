import json
from pathlib import Path

from schemas.user_models import User

USERS_FILE = Path(__file__).parent / "users.json"


def load_users() -> list[User]:
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
        if data:
            return [User.model_validate(x) for x in data]
        else:
            return []


def add_user(user: User):
    users_list = load_users()
    users_list.append(user)

    with open(USERS_FILE, "w") as f:
        json.dump([x.model_dump() for x in users_list], f)


def get_user_by_id(id: int) -> User | None:
    users_list = load_users()
    return next((user for user in users_list if user.id == id), None)


def get_user_by_email(email: str) -> User | None:
    users_list = load_users()
    return next((user for user in users_list if user.email == email), None)


def get_last_user_id() -> int:
    users_list = load_users()
    return users_list[0].id if len(users_list) > 0 else 0
