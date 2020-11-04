from unittest import mock

from app.repositories.user_repo import UserRepo
from app.responses import FailureType, SuccessType
from app.use_cases.create_access_token import CreateAccessToken
from tests.test_data.user_data_provider import UserDataProvider

test_data = UserDataProvider()


def test_create_access_token_success():
    """
    When creating a new access_token,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=UserRepo)
    access_token = test_data.encoded_jwt
    form_data = test_data.password_request_form
    use_case = CreateAccessToken(user_repo=repo)

    repo.authenticate_user.return_value = test_data.sample_user
    repo.create_access_token.return_value = access_token
    response = use_case.execute(form_data)

    assert response.type == SuccessType.CREATED
    assert response.value == test_data.token


def test_create_access_token_failure():
    """
    When creating a new access_token,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=UserRepo)
    repo.authenticate_user.return_value = test_data.sample_user
    repo.create_access_token.side_effect = Exception()
    form_data = test_data.password_request_form
    use_case = CreateAccessToken(user_repo=repo)

    response = use_case.execute(form_data)

    assert response.type == FailureType.RESOURCE_ERROR


def test_create_access_token_authentication_failure():
    """
    When creating a new access_token,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=UserRepo)
    repo.authenticate_user.return_value = None
    form_data = test_data.password_request_form
    use_case = CreateAccessToken(user_repo=repo)

    response = use_case.execute(form_data)

    assert response.type == FailureType.UNAUTHORISED_ERROR
    assert response.message == "Incorrect username or password"
