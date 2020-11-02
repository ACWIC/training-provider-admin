from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.config import settings
from app.domain.entities.user import Token, User
from app.repositories.s3_user_repo import S3UserRepo
from app.requests.user_requests import CreateUserRequest
from app.use_cases.create_user import CreateNewUser

router = APIRouter()
repo = S3UserRepo()


@router.post("/user")
def create_user(inputs: CreateUserRequest) -> Any:
    """
    Create new user.
    """
    use_case = CreateNewUser(user_repo=repo)
    response = use_case.execute(inputs)
    return response


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = repo.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = repo.create_access_token(
        subject={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(repo.get_current_active_user)):
    return current_user
