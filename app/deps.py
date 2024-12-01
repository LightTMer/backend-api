from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.settings import app_settings

security = HTTPBearer(scheme_name="Bearer")


def check_token(token: HTTPAuthorizationCredentials | None = Depends(security)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if token.credentials != app_settings.ACCESS_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
