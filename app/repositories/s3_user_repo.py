import json
from typing import Any

import boto3
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.config import settings
from app.domain.entities.user import TokenData, User
from app.repositories.user_repo import UserRepo
from app.security import oauth2_scheme
from app.utils.error_handling import handle_s3_errors


class S3UserRepo(UserRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with handle_s3_errors():
            self.s3 = boto3.client("s3", **settings.s3_configuration)

    def create_user(self, user_dict: dict) -> User:
        password = user_dict.pop("password", None)
        user_dict["hashed_password"] = self.get_password_hash(password)
        user = User(**user_dict)
        with handle_s3_errors():
            self.s3.put_object(  # Write to bucket
                Body=user.serialize(),
                Key=f"users/{user.username}.json",
                Bucket=settings.USER_BUCKET,
            )

        return user

    def get_user(self, username: str):
        with handle_s3_errors():
            user_obj = self.s3.get_object(
                Key=f"users/{username}.json", Bucket=settings.USER_BUCKET
            )

        user = User(**json.loads(user_obj["Body"].read().decode()))
        return user

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(
        self, current_user: User = Depends(get_current_user)
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
