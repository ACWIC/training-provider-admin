import datetime

from app.repositories.s3_user_repo import S3UserRepo
from tests.repositories.test_s3_course_repo import mock_datetime_now
from tests.test_data.user_data_provider import UserDataProvider

repo = S3UserRepo()
test_data = UserDataProvider()


def test_create_access_token():
    with mock_datetime_now(test_data.date, datetime):
        token = repo.create_access_token(test_data.username)
    print(token)
    assert (
        token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MzAyNjE5MjcsInN1YiI6IlRlc3RDbGllbnQifQ"
        ".xeOieix-mS714WxfM7lQ96t-n8QikivVrL2gC4mjzMA"
    )


def test_create_access_token_with_expire():
    expire = datetime.timedelta(seconds=60)
    with mock_datetime_now(test_data.date, datetime):
        token = repo.create_access_token(test_data.username, expire)
    print(token)
    assert (
        token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MzAyNjAxODcsInN1YiI6IlRlc3RDbGllbnQifQ"
        ".63y_69haryN2JuoqzBJ7GeNOmk2EVoI3rXhhGdI-_ss"
    )


def verify_password():
    assert repo.verify_password(test_data.password, test_data.hashed_password) is True


def hash_password():
    assert repo.get_password_hash(test_data.password) == repo.get_password_hash(
        test_data.password
    )
