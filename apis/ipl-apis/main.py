from fastapi import FastAPI

from routers import users, teams, auth

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
