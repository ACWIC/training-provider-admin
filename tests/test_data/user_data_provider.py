import datetime

from fastapi.security import OAuth2PasswordRequestForm

from app.domain.entities.user import Token, User
from app.repositories.s3_user_repo import S3UserRepo
from app.requests.user_requests import CreateUserRequest
from app.responses import ResponseFailure


class UserDataProvider:
    user: User
    username: str
    create_user_request = CreateUserRequest

    def __init__(self):
        user_repo = S3UserRepo()
        self.user_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
        self.password = "123456789"
        self.hashed_password = user_repo.get_password_hash(self.password)
        self.email = "test@email.com"
        self.full_name = "Test Client"
        self.username = "TestClient"
        self.subject = {"sub": self.username}
        date_time_str = "2018-06-29 08:15:27.243860"
        date = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
        self.date = date
        # User Sample
        self.sample_user = User(
            user_id=self.user_id,
            username=self.username,
            email=self.email,
            full_name=self.full_name,
            disabled=False,
            hashed_password=self.hashed_password,
            is_active=True,
            is_superuser=False,
        )

        # CreateUserRequest Sample
        self.sample_create_user_request = CreateUserRequest(
            username=self.username,
            password=self.password,
            email=self.email,
            full_name=self.full_name,
            disabled=False,
            is_active=True,
            is_superuser=False,
        )

        self.password_request_form = OAuth2PasswordRequestForm(
            username=self.username, password=self.password, scope=""
        )

        self.encoded_jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZXN0Q2xpZW50IiwiZXhwIjoxNjA0NTE1NTYwf"
            "Q.EJ8k8KrE1zvJNKlPHl1wHB7Rh9Mz82E_bROzTjl1QdY"
        )

        self.token = Token(access_token=self.encoded_jwt, token_type="bearer")
        self.jwt_decode_return_false = {}
        self.jwt_decode_return_success = {"sub": "TestClient"}
        self.credentials_exception = ResponseFailure.build_from_unauthorised_error(
            message="Could not validate credentials"
        )
