from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.s3_user_repo import S3UserRepo
from app.requests.user_requests import CreateUserRequest
from app.use_cases.create_access_token import CreateAccessToken
from app.use_cases.create_user import CreateNewUser
from app.use_cases.get_current_active_user import get_current_active_user

router = APIRouter()
repo = S3UserRepo()


@router.post("/user")
def create_user(inputs: CreateUserRequest) -> Any:
    """
    Create new user.
    """
    use_case = CreateNewUser(user_repo=repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    use_case = CreateAccessToken(user_repo=repo)
    response = use_case.execute(form_data)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()


@router.get("/users/me/")
async def read_users_me(response=Depends(get_current_active_user)):
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()
