import abc
import datetime
from typing import Any, Union

from fastapi import Depends
from jose import jwt

from app.config import settings
from app.domain.entities.user import User
from app.security import oauth2_scheme, pwd_context


class UserRepo(abc.ABC):
    @staticmethod
    def create_access_token(
        subject: Union[str, Any], expires_delta: datetime.timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @abc.abstractmethod
    def create_user(self, user_dict: dict) -> User:
        """"""

    @abc.abstractmethod
    def get_user(self, username: str):
        """"""

    @abc.abstractmethod
    def authenticate_user(self, username: str, password: str):
        """"""

    @abc.abstractmethod
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        """"""

    @abc.abstractmethod
    async def get_current_active_user(
        self, current_user: User = Depends(get_current_user)
    ):
        """"""
