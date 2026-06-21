from pydantic import BaseModel, Field


class Player(BaseModel):
    name: str = Field(max_length=25)
    jersey_number: int = Field(gt=0, lt=1000)
    total_runs: int = Field(default=0, ge=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Virat kohli",
                    "jersey_number": "18",
                    "total_runs": "18000",
                }
            ]
        }
    }


class TeamAddModel(BaseModel):
    name: str = Field(max_length=30, examples=["Royal challengers banguluru"])
    shortName: str
    HomeCity: str
    HomeGroundName: str
    TotalTrophies: int
    players: list[Player] = []


class Team(TeamAddModel):
    id: int
