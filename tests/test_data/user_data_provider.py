import datetime

from app.domain.entities.user import User
from app.repositories.s3_user_repo import S3UserRepo
from app.requests.user_requests import CreateUserRequest


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
        self.sample_update_user_request = CreateUserRequest(
            username=self.username,
            password=self.password,
            email=self.email,
            full_name=self.full_name,
            disabled=False,
            is_active=True,
            is_superuser=False,
        )
