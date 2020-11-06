from app.domain.entities.user import Token, TokenData, User
from tests.test_data.user_data_provider import UserDataProvider

test_data = UserDataProvider()


def test_user_init():
    """
    Ensure the user data matches constructor values
    and the status is appropriately set.
    """

    user = User(
        user_id=test_data.user_id,
        username=test_data.username,
        email=test_data.email,
        full_name=test_data.full_name,
        disabled=True,
        hashed_password=test_data.hashed_password,
        is_active=False,
        is_superuser=True,
    )

    assert user.user_id == test_data.user_id
    assert user.username == test_data.username
    assert user.email == test_data.email
    assert user.full_name == test_data.full_name
    assert user.disabled is True
    assert user.hashed_password == test_data.hashed_password
    assert user.is_active is False
    assert user.is_superuser is True


def test_user_serialize():
    user = test_data.sample_user
    byte_string = user.serialize()
    assert bytes(test_data.user_id, "utf-8") in byte_string
    assert bytes(test_data.username, "utf-8") in byte_string
    assert bytes(test_data.email, "utf-8") in byte_string


def test_token_init():
    access_token, token_type = "123456789", "test"
    token = Token(access_token=access_token, token_type=token_type)

    assert token.access_token == access_token
    assert token.token_type == token_type


def test_token_data_init():
    username = "TEST"
    token_data = TokenData(username=username)

    assert token_data.username == username
