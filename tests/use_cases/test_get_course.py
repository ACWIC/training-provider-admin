"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.course_repo import CourseRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_course import GetCourseByID
from tests.test_data.course_data_provider import CourseDataProvider


def test_get_course_success():
    """
    When getting a course,
    if everything goes according to plan,
    the response type should be "Success".
    """
    course_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    repo = mock.Mock(spec=CourseRepo)
    course = CourseDataProvider().sample_course
    use_case = GetCourseByID(course_repo=repo)

    repo.get_course.return_value = course
    response = use_case.execute(course_id)

    assert response.type == SuccessType.SUCCESS


def test_get_course_not_exists():
    repo = mock.Mock(spec=CourseRepo)
    course_id = CourseDataProvider().sample_course_id
    repo.course_exists.return_value = False
    repo.get_course.return_value = CourseDataProvider().sample_course

    use_case = GetCourseByID(course_repo=repo)
    response = use_case.execute(course_id)

    assert response.type == FailureType.VALIDATION_ERROR


def test_get_course_failure():
    """
    When getting a course,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    course_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    repo = mock.Mock(spec=CourseRepo)
    repo.get_course.side_effect = Exception()
    use_case = GetCourseByID(course_repo=repo)

    response = use_case.execute(course_id)

    assert response.type == FailureType.RESOURCE_ERROR
