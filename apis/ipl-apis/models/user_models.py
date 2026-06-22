from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str = Field(max_length=25, index=True)
    email: EmailStr = Field(index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str = Field()


class UserInput(UserBase):
    password: str


class UserLoginInput(BaseModel):
    email: EmailStr
    password: str


class Tokens(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None
