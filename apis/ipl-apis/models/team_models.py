from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=25)
    jersey_number: int
    total_runs: int = Field(default=0)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="players")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, unique=True, index=True)
    short_name: str
    home_city: str
    home_ground_name: str
    total_trophies: int
    players: list[Player] = Relationship(back_populates="team")
