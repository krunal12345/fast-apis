class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.message = f"User with email '{email}' already exists"
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __int__(self, detail: str | int):
        self.message = f"User with email or Id {detail} Not found"
