from unittest import mock

from fastapi.testclient import TestClient

from app.domain.entities.industry_standard import IndustryStandard
from app.main import app
from app.responses import FailureType, ResponseFailure, ResponseSuccess, SuccessType
from tests.test_data.standards_data_provider import StandardsDataProvider

test_data = StandardsDataProvider()
client = TestClient(app)


@mock.patch("app.use_cases.post_industry_standard.PostIndustryStandard")
def test_post_industry_standard_success(use_case):
    code = SuccessType.CREATED
    message = "The industry_standard has been created."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.industry_standard,
        type=code,
        message=message,
    )
    data = test_data.industry_standard_request
    response = client.post("/industry_standards", data=data.json())

    json_result = response.json()
    standard = IndustryStandard(**json_result.get("value"))
    standard.standard_id = test_data.industry_standard.standard_id

    assert json_result.get("message") == message
    assert json_result.get("type") == SuccessType.CREATED.value
    assert standard == test_data.industry_standard
    use_case().execute.assert_called_with(data)


@mock.patch("app.use_cases.post_industry_standard.PostIndustryStandard")
def test_post_industry_standard_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    data = test_data.industry_standard_request
    response = client.post("/industry_standards", data=data.json())

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}


@mock.patch("app.use_cases.delete_industry_standard.DeleteIndustryStandard")
def test_delete_industry_standard_success(use_case):
    code = SuccessType.SUCCESS
    message = "The industry_standard has been deleted."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.delete_standard_response,
        type=code,
        message=message,
    )

    response = client.delete(
        f"/industry_standards/{test_data.industry_standard.standard_id}",
    )
    json_result = response.json()

    assert json_result.get("message") == message
    assert json_result.get("type") == SuccessType.SUCCESS.value
    assert json_result.get("value") == test_data.delete_standard_response


@mock.patch("app.use_cases.delete_industry_standard.DeleteIndustryStandard")
def test_delete_industry_standard_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    response = client.delete(
        f"/industry_standards/{test_data.industry_standard.standard_id}",
    )

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}


@mock.patch("app.use_cases.get_industry_standards.GetIndustryStandards")
def test_get_industry_standards_success(use_case):
    code = SuccessType.SUCCESS
    message = "The industry_standard has been fetched."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.industry_standard_list,
        type=code,
        message=message,
    )
    response = client.get("/industry_standards")
    json_result = response.json()

    assert json_result.get("message") == message
    assert json_result.get("type") == SuccessType.SUCCESS.value
    assert json_result.get("value") == test_data.industry_standard_list


@mock.patch("app.use_cases.get_industry_standards.GetIndustryStandards")
def test_get_industry_standards_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    response = client.get("/industry_standards")

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}
