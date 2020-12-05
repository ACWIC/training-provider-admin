from unittest import mock

from fastapi.testclient import TestClient

from app.domain.entities.enrolment_request import EnrolmentAuth
from app.main import app
from app.responses import FailureType, ResponseFailure, ResponseSuccess, SuccessType
from app.security import oauth2_scheme
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()
client = TestClient(app)


async def override_dependency():
    return "TEST-JWT-TOKEN"


app.dependency_overrides[oauth2_scheme] = override_dependency


@mock.patch("app.use_cases.get_enrolments.GetEnrolmentAuths")
def test_get_enrolments_success(use_case):
    message = "The enrolment requests have been fetched."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_result,
        message=message,
    )

    params = test_data.sample_enrolment_auth_filters
    response = client.get("/enrolment_requests", params=params.dict())
    json_result = response.json()
    enrolments = json_result.get("value").get("enrolments")
    enrolment = EnrolmentAuth(**enrolments[0])
    enrolment1 = EnrolmentAuth(**enrolments[1])

    use_case().execute.assert_called_with(test_data.sample_enrolment_auth_filters_json)
    assert response.status_code == SuccessType.SUCCESS.value
    assert enrolment == test_data.sample_enrolment_auth
    assert enrolment1 == test_data.sample_enrolment_auth1
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_enrolments.GetEnrolmentAuths")
def test_get_enrolments_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    params = test_data.sample_enrolment_auth_filters
    response = client.get("/enrolment_requests", params=params.dict())

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}


@mock.patch("app.use_cases.process_enrolments.ProcessEnrolmentAuths")
def test_process_enrolments_success(use_case):
    message = "The enrolment's state has been changed."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_enrolment_auth,
        message=message,
    )

    request = test_data.process_enrolment_request.dict()
    params = {"new_state": request["new_state"]}
    response = client.patch(
        f"/enrolment_requests/{test_data.enrolment_id}", params=params
    )
    json_result = response.json()
    enrolment = EnrolmentAuth(**json_result.get("value"))

    use_case().execute.assert_called_with(test_data.process_enrolment_request)
    assert response.status_code == SuccessType.SUCCESS.value
    assert enrolment == test_data.sample_enrolment_auth
    assert json_result.get("message") == message


@mock.patch("app.use_cases.process_enrolments.ProcessEnrolmentAuths")
def test_process_enrolments_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    params = test_data.process_enrolment_request.dict()
    response = client.patch(
        f"/enrolment_requests/{test_data.enrolment_id}", params=params
    )

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}
