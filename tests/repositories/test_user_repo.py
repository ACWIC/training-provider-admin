import datetime
import time

from app.repositories.s3_user_repo import S3UserRepo
from tests.test_data.user_data_provider import UserDataProvider

repo = S3UserRepo()
test_data = UserDataProvider()


def test_create_access_token():
    token = repo.create_access_token(test_data.username)
    time.sleep(1)
    token_2 = repo.create_access_token(test_data.username)
    assert len(token) == 131
    assert token != token_2


def test_create_access_token_with_expire():
    expire = datetime.timedelta(seconds=60)
    token_with_expired = repo.create_access_token(test_data.username, expire)
    token = repo.create_access_token(test_data.username)
    time.sleep(1)
    token_with_expired_2 = repo.create_access_token(test_data.username, expire)

    assert len(token_with_expired) == 131
    assert token_with_expired != token
    assert token_with_expired != token_with_expired_2


def verify_password():
    verify = repo.verify_password(test_data.password, test_data.hashed_password)
    assert verify is True

    verify = repo.verify_password("random_password", test_data.hashed_password)
    assert verify is False


def hash_password():
    assert repo.get_password_hash(test_data.password) == repo.get_password_hash(
        test_data.password
    )
