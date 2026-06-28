from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
    SecurityScopes,
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
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"teams": "you can access teams", "users": "you can access users"},
)


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


def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
) -> UserBase:
    try:
        claims = jwt.decode(
            token,
            "JustRandomJWTLearningString",
            algorithms=["HS256"],
        )

        token_scopes: str = claims.get("scopes", "")
        scopes: list[str] = token_scopes.split(" ")

    except Exception:
        print("came into the expection")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if not scopes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="valid scope is not provided",
        )

    for scope in security_scopes.scopes:
        print(scope not in scopes, "condition")
        if scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="valid scope is not provided",
            )

    return UserBase(id=claims["id"], email=claims["sub"], name=claims["username"])
