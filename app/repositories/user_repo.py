import abc
import datetime

from jose import JWTError, jwt

from app.config import settings
from app.domain.entities.user import User
from app.security import pwd_context


class UserRepo(abc.ABC):
    @staticmethod
    def create_access_token(
        subject: dict, expires_delta: datetime.timedelta = None
    ) -> str:
        to_encode = subject.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(
                to_encode, settings.SECRET_TOKEN_KEY, algorithm=settings.ALGORITHM
            )
        except JWTError as e:
            raise Exception(
                f"JWT Encoding Error. Please check the full error message: {e}"
            )
        return encoded_jwt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)  # noqa

    @abc.abstractmethod
    def create_user(self, user_dict: dict) -> User:
        """"""

    @abc.abstractmethod
    def get_user(self, username: str):
        """"""

    @abc.abstractmethod
    def authenticate_user(self, username: str, password: str):
        """"""
