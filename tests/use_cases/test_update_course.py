"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.course_repo import CourseRepo
from app.use_cases.update_course import UpdateCourse
from tests.test_data.course_data_provider import CourseDataProvider


def test_update_course_success():
    """
    When updating a course,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=CourseRepo)
    course = CourseDataProvider().sample_course
    request = CourseDataProvider().sample_update_course_request
    use_case = UpdateCourse(course_repo=repo)

    repo.update_course.return_value = course
    response = use_case.execute(request)

    assert response.type == "Success"


def test_update_course_failure():
    """
    When updating a course,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CourseRepo)
    repo.update_course.side_effect = Exception()
    request = CourseDataProvider().sample_update_course_request
    use_case = UpdateCourse(course_repo=repo)
    response = use_case.execute(request)

    assert response.type == "ResourceError"
