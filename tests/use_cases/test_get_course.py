"""
These tests evaluate (and document) the business logic.
"""
import datetime
from unittest import mock
from uuid import uuid4

from app.domain.entities.course import Course
from app.repositories.course_repo import CourseRepo
from app.use_cases.get_course import GetCourseByID


def test_get_course_success():
    """
    When creating a new enrollment authorisation,
    if everything goes according to plan,
    the response type should be "Success".
    """
    course_id = str(uuid4())
    created = str(datetime.datetime.now())
    repo = mock.Mock(spec=CourseRepo)
    course = Course(
        course_id=course_id,
        course_name="Bachelor of Community Services (HE20528)",
        industry_standards="Police Check",
        competancy="top rated",
        location="Sydney",
        date="2020-10-11T16:06:53.739338",
        availablity="morning",
        hours_per_week="10",
        duration="2 months",
        fees_from="200",
        created=created,
    )
    repo.get_course.return_value = course

    use_case = GetCourseByID(course_repo=repo)
    response = use_case.execute(course_id)

    assert response.type == "Success"


def test_get_course_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    course_id = str(uuid4())
    repo = mock.Mock(spec=CourseRepo)

    repo.get_course.side_effect = Exception()

    use_case = GetCourseByID(course_repo=repo)
    response = use_case.execute(course_id)

    assert response.type == "ResourceError"
