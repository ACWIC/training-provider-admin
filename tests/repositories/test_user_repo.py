import datetime
import time
from unittest import mock

from app.config import settings
from app.repositories.s3_user_repo import S3UserRepo
from tests.test_data.user_data_provider import UserDataProvider

repo = S3UserRepo()
test_data = UserDataProvider()


def test_create_access_token():
    token = repo.create_access_token(test_data.subject)
    time.sleep(1)
    token_2 = repo.create_access_token(test_data.subject)
    assert len(token) == 131
    assert token != token_2


def test_create_access_token_with_expire():
    expire = datetime.timedelta(seconds=60)
    token_with_expired = repo.create_access_token(test_data.subject, expire)
    token = repo.create_access_token(test_data.subject)
    time.sleep(1)
    token_with_expired_2 = repo.create_access_token(test_data.subject, expire)

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


@mock.patch("boto3.client")
def test_create_user(boto_client):
    rep = S3UserRepo()
    user = rep.create_user(test_data.sample_update_user_request.dict())

    assert user.username == test_data.sample_user.username
    assert user.email == test_data.sample_user.email
    assert user.full_name == test_data.sample_user.full_name
    boto_client.return_value.put_object.assert_called_once_with(
        Body=user.serialize(),
        Key=f"users/{user.username}.json",
        Bucket=settings.USER_BUCKET,
    )


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_user(boto_client, json_loads):
    rep = S3UserRepo()
    username = test_data.username
    json_loads.return_value = test_data.sample_user.dict()
    user = rep.get_user(username)

    assert user == test_data.sample_user
    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"users/{username}.json", Bucket=settings.USER_BUCKET
    )


def authenticate_user_get_user_false():
    rep = mock.Mock(spec=S3UserRepo)
    rep.return_value.get_user = None
    assert rep.authenticate_user(test_data.username, test_data.password) is False


def authenticate_user_verify_password_false():
    rep = mock.Mock(spec=S3UserRepo)
    rep.return_value.get_user = test_data.sample_user
    rep.return_value.verify_password = False
    assert rep.authenticate_user(test_data.username, test_data.password) is False


def authenticate_user_success():
    rep = mock.Mock(spec=S3UserRepo)
    rep.return_value.get_user = test_data.sample_user
    rep.return_value.verify_password = True
    assert (
        rep.authenticate_user(test_data.username, test_data.password)
        == test_data.sample_user
    )
