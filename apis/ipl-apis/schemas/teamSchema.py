from pydantic import BaseModel


class TeamAddModel(BaseModel):
    name: str
    shortName: str
    HomeCity: str
    HomeGroundName: str
    TotalTrophies: int


class Team(TeamAddModel):
    id: int
