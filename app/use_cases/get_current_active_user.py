from fastapi import Depends
from jose import JWTError, jwt

from app.config import settings
from app.domain.entities.user import TokenData, User
from app.repositories.s3_user_repo import S3UserRepo
from app.responses import ResponseFailure, ResponseSuccess
from app.security import oauth2_scheme

repo = S3UserRepo()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = ResponseFailure.build_from_unauthorised_error(
        message="Could not validate credentials"
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = repo.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        return ResponseFailure.build_from_resource_error(message="Inactive user")

    return ResponseSuccess(value=current_user)
