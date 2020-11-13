import unittest
from unittest import mock

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient

from app.domain.entities.user import Token, User
from app.main import app
from app.responses import FailureType, ResponseFailure, ResponseSuccess, SuccessType
from app.use_cases.get_current_active_user import get_current_active_user
from tests.test_data.user_data_provider import UserDataProvider

test_data = UserDataProvider()


async def override_dependencies():
    return test_data.password_request_form


async def override_users_me_success():
    return ResponseSuccess(value=test_data.sample_user)


async def override_users_me_failure():
    return ResponseFailure.build_from_unauthorised_error(message="Error")


app.dependency_overrides[OAuth2PasswordRequestForm] = override_dependencies


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.dependencies = app.dependency_overrides.copy()

    def tearDown(self) -> None:
        app.dependency_overrides = self.dependencies

    @mock.patch("app.use_cases.create_user.CreateNewUser")
    def test_create_user_success(self, use_case):
        code = SuccessType.CREATED
        message = "The user has been created."
        use_case().execute.return_value = ResponseSuccess(
            value=test_data.sample_user,
            type=code,
            message=message,
        )

        data = test_data.sample_create_user_request
        response = self.client.post("/user", data=data.json())
        json_result = response.json()
        user = User(**json_result.get("value"))

        use_case().execute.assert_called_with(data)
        assert response.status_code == SuccessType.CREATED.value
        assert user == test_data.sample_user
        assert json_result.get("message") == message

    @mock.patch("app.use_cases.create_user.CreateNewUser")
    def test_create_user_failure(self, use_case):
        message = "Error"
        use_case().execute.return_value = ResponseFailure.build_from_resource_error(
            message=message,
        )

        data = test_data.sample_create_user_request
        response = self.client.post("/user", data=data.json())

        assert response.status_code == FailureType.RESOURCE_ERROR.value
        assert response.json() == {"detail": "RESOURCE_ERROR: " + message}

    @mock.patch("app.use_cases.create_access_token.CreateAccessToken")
    def test_login_for_access_token_success(self, use_case):
        message = "Token is created."
        code = SuccessType.CREATED
        use_case().execute.return_value = ResponseSuccess(
            value=test_data.token,
            message=message,
            type=code,
        )

        response = self.client.post("/token")
        json_result = response.json()
        token = Token(**json_result.get("value"))

        use_case().execute.assert_called_with(test_data.password_request_form)
        assert response.status_code == SuccessType.CREATED.value
        assert token == test_data.token
        assert json_result.get("message") == message

    @mock.patch("app.use_cases.create_access_token.CreateAccessToken")
    def test_login_for_access_token_failure(self, use_case):
        message = "Error"
        use_case().execute.return_value = ResponseFailure.build_from_unauthorised_error(
            message=message,
        )

        response = self.client.post("/token")

        assert response.status_code == FailureType.UNAUTHORISED_ERROR.value
        assert response.json() == {"detail": "UNAUTHORISED_ERROR: " + message}

    def test_read_users_me_success(self):
        app.dependency_overrides[get_current_active_user] = override_users_me_success

        response = self.client.get("/users/me")
        json_result = response.json()
        user = User(**json_result.get("value"))

        assert response.status_code == SuccessType.SUCCESS.value
        assert user == test_data.sample_user

    def test_read_users_me_failure(self):
        message = "Error"
        app.dependency_overrides[get_current_active_user] = override_users_me_failure

        response = self.client.get("/users/me")

        assert response.status_code == FailureType.UNAUTHORISED_ERROR.value
        assert response.json() == {"detail": "UNAUTHORISED_ERROR: " + message}
