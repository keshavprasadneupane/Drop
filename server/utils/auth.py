from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from fastapi import Security, Depends, status, HTTPException
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes)
from env_config import Config


SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.HASH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(Config.TOKEN_EXPIRY)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def create_access_token(data: dict):
    details = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    details.update({"exp": expiry})
    return jwt.encode(
        details,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception