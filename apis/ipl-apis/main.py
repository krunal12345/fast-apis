from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from routers import users, teams, auth

from exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from models.user_models import Tokens, UserInput
import services.user_service as user_service
from utils.dependencies import UoWDep
from utils.user_utils import create_db_and_tables

app = FastAPI()

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "this is the IPL api learning project"}


@app.get("/health")
def halth():
    return {"ok"}
