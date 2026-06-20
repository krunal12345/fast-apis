class TeamAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.message = f"Team with name '{name}' already exists"
        super().__init__(self.message)


class TeamNotFoundError(Exception):
    def __init__(self, team_id: int):
        self.message = f"Team with id '{team_id}' not found"
        super().__init__(self.message)
