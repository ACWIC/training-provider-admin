"""
These tests evaluate (and document) the business logic.
"""
import datetime
from unittest import mock
from uuid import uuid4

from app.domain.entities.course import Course
from app.repositories.course_repo import CourseRepo
from app.requests.create_course_request import NewCourseRequest
from app.use_cases.create_course import CreateNewCourse


def test_create_course_success():
    """
    When creating a new enrollment authorisation,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=CourseRepo)
    course_id = str(uuid4())
    created = str(datetime.datetime.now())
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
    repo.save_course.return_value = course

    request = NewCourseRequest(
        course_name="Bachelor of Community Services (HE20528)",
        industry_standards="Police Check",
        competancy="top rated",
        location="Sydney",
        date="2020-10-11T16:06:53.739338",
        availablity="morning",
        hours_per_week="10",
        duration="2 months",
        fees_from="200",
    )
    use_case = CreateNewCourse(course_repo=repo)
    response = use_case.execute(request)

    assert response.type == "Success"


def test_create_course_failure():
    """
    When creating a new enrollment authorisation,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=CourseRepo)

    repo.save_course.side_effect = Exception()
    request = NewCourseRequest(
        course_name="Bachelor of Community Services (HE20528)",
        industry_standards="Police Check",
        competancy="top rated",
        location="Sydney",
        date="2020-10-11T16:06:53.739338",
        availablity="morning",
        hours_per_week="10",
        duration="2 months",
        fees_from="200",
    )
    use_case = CreateNewCourse(course_repo=repo)
    response = use_case.execute(request)

    assert response.type == "ResourceError"
