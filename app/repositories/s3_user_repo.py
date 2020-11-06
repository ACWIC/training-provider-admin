import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.user import User
from app.repositories.user_repo import UserRepo
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
