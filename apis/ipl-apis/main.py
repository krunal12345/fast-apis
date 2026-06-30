from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers import users, teams, auth

from utils.user_utils import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "this is the IPL api learning project"}


@app.get("/health")
def halth():
    return {"ok"}
