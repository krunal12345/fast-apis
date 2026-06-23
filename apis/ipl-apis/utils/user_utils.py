from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
import jwt

from schemas.user_models import UserBase
from sqlmodel import SQLModel, create_engine

database_name = "ipldatabase.db"
database_url = f"sqlite:///{database_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(database_url, connect_args=connect_args)


def create_db_and_tables():
    # Side-effect imports: registers both model files with SQLModel metadata
    # before create_all runs — without these, tables may not be created.
    __import__("models.user_models")
    __import__("models.team_models")
    SQLModel.metadata.create_all(engine)


security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        claims = jwt.decode(
            credentials.credentials,
            "JustRandomJWTLearningString",
            algorithms=["HS256"],
        )
        return claims
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserBase:
    try:
        claims = jwt.decode(
            token,
            "JustRandomJWTLearningString",
            algorithms=["HS256"],
        )
        return UserBase(id=claims["id"], email=claims["sub"], name=claims["username"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
