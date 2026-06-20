import json
from pathlib import Path
from schemas.teamSchema import Team, TeamAddModel

TEAMS_FILE = Path(__file__).parent / "teams.json"


def loadTeamsData() -> list[Team]:
    with open(TEAMS_FILE, "r") as f:
        raw = json.load(f)  # list of dicts
        return [Team.model_validate(item) for item in raw]  # list of Team objects


def saveJsondata(data: list[Team]):
    with open(TEAMS_FILE, "w") as f:
        json.dump([item.model_dump() for item in data], f, indent=4)


def find_by_name(name: str) -> Team | None:
    data = loadTeamsData()
    return next((t for t in data if t.name == name), None)


def find_by_id(id: int) -> Team | None:
    data = loadTeamsData()
    return next((t for t in data if t.id == id), None)


def addTeam(team: TeamAddModel):
    data = loadTeamsData()
    teamId = data[-1].id + 1 if data else 1
    data.append(Team(id=teamId, **team.model_dump()))
    saveJsondata(data)
    return
