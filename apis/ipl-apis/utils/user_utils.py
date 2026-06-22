from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
import jwt

from schemas.user_models import UserBase

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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserBase:

    claims = jwt.decode(
        token,
        "JustRandomJWTLearningString",
        algorithms=["HS256"],
    )

    return UserBase(id=claims["id"], email=claims["sub"], name=claims["username"])
