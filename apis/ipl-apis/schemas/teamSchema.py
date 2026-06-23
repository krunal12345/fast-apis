from pydantic import BaseModel, ConfigDict, Field


class PlayerSchema(BaseModel):
    """Used for both API input (adding players) and API output (team responses)."""

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=25)
    jersey_number: int = Field(gt=0, lt=1000)
    total_runs: int = Field(default=0, ge=0)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {"name": "Virat Kohli", "jersey_number": 18, "total_runs": 18000}
            ]
        },
    }


class TeamAddModel(BaseModel):
    """Request body for creating a new team."""

    name: str = Field(max_length=30, examples=["Royal Challengers Bangalore"])
    short_name: str
    home_city: str
    home_ground_name: str
    total_trophies: int


class TeamResponse(BaseModel):
    """Response schema for team data. Reads directly from ORM objects."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    short_name: str
    home_city: str
    home_ground_name: str
    total_trophies: int
    players: list[PlayerSchema] = []
