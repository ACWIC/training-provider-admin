from unittest import mock

from app.repositories.user_repo import UserRepo
from app.responses import FailureType, SuccessType
from app.use_cases.create_user import CreateNewUser
from tests.test_data.user_data_provider import UserDataProvider

test_data = UserDataProvider()


def test_create_user_success():
    """
    When creating a new user,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=UserRepo)
    user = test_data.sample_user
    request = test_data.sample_create_user_request
    use_case = CreateNewUser(user_repo=repo)

    repo.create_user.return_value = user
    response = use_case.execute(request)

    assert response.type == SuccessType.CREATED
    assert response.value == user


def test_create_user_failure():
    """
    When creating a new user,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=UserRepo)
    repo.create_user.side_effect = Exception()
    request = test_data.sample_create_user_request
    use_case = CreateNewUser(user_repo=repo)

    response = use_case.execute(request)

    assert response.type == FailureType.RESOURCE_ERROR
