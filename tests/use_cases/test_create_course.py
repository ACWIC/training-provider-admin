"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.course_repo import CourseRepo
from app.responses import FailureType, SuccessType
from app.use_cases.create_course import CreateNewCourse
from tests.test_data.course_data_provider import CourseDataProvider


def test_create_course_success():
    """
    When creating a new course,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=CourseRepo)
    course = CourseDataProvider().sample_course
    request = CourseDataProvider().sample_create_course_request
    use_case = CreateNewCourse(course_repo=repo)

    repo.create_course.return_value = course
    response = use_case.execute(request)

    assert response.type == SuccessType.SUCCESS


def test_create_course_failure():
    """
    When creating a new course,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CourseRepo)
    repo.create_course.side_effect = Exception()
    request = CourseDataProvider().sample_create_course_request
    use_case = CreateNewCourse(course_repo=repo)

    response = use_case.execute(request)

    assert response.type == FailureType.RESOURCE_ERROR
