from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()


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
