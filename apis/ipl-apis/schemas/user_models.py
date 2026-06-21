from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: int
    name: str = Field(max_length=25)
    email: EmailStr


class User(UserBase):
    password_hash: str


class UserInput(UserBase):
    password: str
