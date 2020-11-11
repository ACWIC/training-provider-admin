from unittest import mock

import pytest
from jose import JWTError

import app.use_cases.get_current_active_user as uc
from app.responses import FailureType
from tests.test_data.user_data_provider import UserDataProvider

test_data = UserDataProvider()


@pytest.mark.asyncio
@mock.patch("app.use_cases.get_current_active_user.jwt")
@mock.patch("app.use_cases.get_current_active_user.repo")
def test_get_current_user_success(repo, jwt, event_loop):
    """
    When creating a new user,
    if everything goes according to plan,
    the response type should be "Success".
    """
    jwt.decode.return_value = test_data.jwt_decode_return_success
    repo.get_user.return_value = test_data.sample_user
    user = event_loop.run_until_complete(uc.get_current_user())

    assert user.username == test_data.username
    assert user.email == test_data.email
    assert user.full_name == test_data.full_name
    assert user.disabled is False
    assert user.is_active is True
    assert user.is_superuser is False


@pytest.mark.asyncio
@mock.patch("app.use_cases.get_current_active_user.jwt")
@mock.patch("app.use_cases.get_current_active_user.repo")
def test_get_current_user_returns_none(repo, jwt, event_loop):
    """
    When creating a new user,
    if everything goes according to plan,
    the response type should be "Success".
    """
    jwt.decode.return_value = test_data.jwt_decode_return_success
    repo.get_user.return_value = None
    user = event_loop.run_until_complete(uc.get_current_user())
    assert not user


@pytest.mark.asyncio
@mock.patch("app.use_cases.get_current_active_user.jwt")
def test_get_current_user_username_faiure(jwt, event_loop):
    """
    When creating a new user,
    if everything goes according to plan,
    the response type should be "Success".
    """
    jwt.decode.return_value = test_data.jwt_decode_return_false
    response = event_loop.run_until_complete(uc.get_current_user())

    assert response.type == FailureType.UNAUTHORISED_ERROR
    assert response.message == "UNAUTHORISED_ERROR: Could not validate credentials"


@pytest.mark.asyncio
@mock.patch("app.use_cases.get_current_active_user.jwt")
def test_get_current_user_jwt_decode_failure(jwt, event_loop):
    """
    When creating a new user,
    if everything goes according to plan,
    the response type should be "Success".
    """
    jwt.decode.side_effect = JWTError
    response = event_loop.run_until_complete(uc.get_current_user())

    assert response.type == FailureType.UNAUTHORISED_ERROR
    assert response.message == "UNAUTHORISED_ERROR: Could not validate credentials"
