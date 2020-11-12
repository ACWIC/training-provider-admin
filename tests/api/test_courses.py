from unittest import mock

from fastapi.testclient import TestClient

from app.domain.entities.course import Course
from app.main import app
from app.responses import FailureType, ResponseFailure, ResponseSuccess, SuccessType
from app.security import oauth2_scheme
from tests.test_data.course_data_provider import CourseDataProvider

test_data = CourseDataProvider()
client = TestClient(app)


async def override_dependency():
    return "TEST-JWT-TOKEN"


app.dependency_overrides[oauth2_scheme] = override_dependency


@mock.patch("app.use_cases.create_course.CreateNewCourse")
def test_create_course_success_created(use_case):
    code = SuccessType.CREATED
    message = "The course has been created."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_course,
        type=code,
        message=message,
    )

    data = test_data.sample_create_course_request
    response = client.post("/course", data=data.json())
    json_result = response.json()
    course = Course(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.CREATED.value
    assert course == test_data.sample_course
    assert json_result.get("message") == message


@mock.patch("app.use_cases.create_course.CreateNewCourse")
def test_create_course_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    data = test_data.sample_create_course_request
    response = client.post("/course", data=data.json())

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}


@mock.patch("app.use_cases.update_course.UpdateCourse")
def test_update_course_success(use_case):
    message = "The callback has been fetched from the server."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_updated_course,
        message=message,
    )

    data = test_data.sample_update_course_request
    response = client.put("/course", data=data.json())
    json_result = response.json()
    course = Course(**json_result.get("value"))

    use_case().execute.assert_called_with(data)
    assert response.status_code == SuccessType.SUCCESS.value
    assert course != test_data.sample_course
    assert course == test_data.sample_updated_course
    assert json_result.get("message") == message


@mock.patch("app.use_cases.update_course.UpdateCourse")
def test_update_course_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    data = test_data.sample_update_course_request
    response = client.put("/course", data=data.json())

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}


@mock.patch("app.use_cases.get_course.GetCourseByID")
def test_get_course_by_id_success(use_case):
    message = "The callback has been fetched from the server."
    use_case().execute.return_value = ResponseSuccess(
        value=test_data.sample_course,
        message=message,
    )

    response = client.get(f"/course/{test_data.sample_course_id}")
    json_result = response.json()
    course = Course(**json_result.get("value"))

    use_case().execute.assert_called_with(test_data.sample_course_id)
    assert response.status_code == SuccessType.SUCCESS.value
    assert course == test_data.sample_course
    assert json_result.get("message") == message


@mock.patch("app.use_cases.get_course.GetCourseByID")
def test_get_course_by_id_failure(use_case):
    message = "Error"
    use_case().execute.return_value = ResponseFailure.build_from_resource_error(
        message=message,
    )

    response = client.get(f"/course/{test_data.sample_course_id}")

    assert response.status_code == FailureType.RESOURCE_ERROR.value
    assert response.json() == {"detail": "RESOURCE_ERROR: " + message}
