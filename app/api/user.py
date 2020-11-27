from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.s3_user_repo import S3UserRepo
from app.requests.user_requests import CreateUserRequest
from app.use_cases import create_access_token as cat
from app.use_cases import create_user as cu
from app.use_cases import get_current_active_user as gcau

router = APIRouter()
repo = S3UserRepo()


@router.post("/user")
def create_user(inputs: CreateUserRequest) -> Any:
    """
    Create new user.\n
    This API is used to create a new user for the
    purpose of authentication and authourization
    so that each user has only the required access.\n
    <b>username</b> should be unique to identify the user.
    It is a required field.\n
    <b>password</b> is a required field as well.\n
    <b>email</b> is optional for contact purposes.\n
    <b>full_name</b> is Optional.\n
    <b>disabled</b> field is a boolean (True or False).
    It tells if the user is disabled or not.
    It is Optional.\n
    <b>is_active</b> is a boolean and defaults to True.
    It is Optional.\n
    <b>is_superuser</b> is a boolean and defaults to False.
    It is Optional. \n
    """
    use_case = cu.CreateNewUser(user_repo=repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests.\n
    This API is used to login the user. The user enters username and
    password to login.\n
    <b>username</b> is required to login.\n
    <b>password</b> for the username is required\n
    Other fields are for OAuth2 compatibility.
    """
    use_case = cat.CreateAccessToken(user_repo=repo)
    response = use_case.execute(form_data)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()


@router.get("/users/me/")
async def read_users_me(response=Depends(gcau.get_current_active_user)):
    """
    This API returns the information of the current user
    using the jwt token provided through login.\n
    """
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()
