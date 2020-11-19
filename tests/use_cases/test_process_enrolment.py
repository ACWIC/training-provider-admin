"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.course_repo import CourseRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.process_enrolments import ProcessEnrolments
from tests.test_data.course_data_provider import CourseDataProvider
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()
course_test_data = CourseDataProvider()


def test_get_enrolments_success():
    enrolment_filters = test_data.sample_enrolment_filters.dict()
    repo = mock.Mock(spec=EnrolmentRepo)
    course_repo = mock.Mock(spec=CourseRepo)
    enrolment = test_data.sample_enrolment
    use_case = ProcessEnrolments(enrolment_repo=repo, course_repo=course_repo)

    repo.get_enrolments.return_value = [enrolment]
    course_repo.course_exists.return_value = True
    course_repo.get_course.return_value = course_test_data.sample_course
    response = use_case.execute(enrolment_filters)

    assert response.type == SuccessType.SUCCESS


def test_get_enrolments_course_not_exists():
    enrolment_filters = test_data.sample_enrolment_filters.dict()
    repo = mock.Mock(spec=EnrolmentRepo)
    course_repo = mock.Mock(spec=CourseRepo)
    course_repo.course_exists.return_value = False

    use_case = ProcessEnrolments(enrolment_repo=repo, course_repo=course_repo)
    response = use_case.execute(enrolment_filters)

    assert response.type == FailureType.VALIDATION_ERROR


def test_get_enrolments_failure():
    enrolment_filters = test_data.sample_enrolment_filters.dict()
    repo = mock.Mock(spec=EnrolmentRepo)
    course_repo = mock.Mock(spec=CourseRepo)
    use_case = ProcessEnrolments(enrolment_repo=repo, course_repo=course_repo)

    repo.get_enrolments.side_effect = Exception()
    course_repo.course_exists.return_value = True
    course_repo.get_course.return_value = course_test_data.sample_course
    response = use_case.execute(enrolment_filters)

    assert response.type == FailureType.RESOURCE_ERROR
