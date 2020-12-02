"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_enrolments import GetEnrolments
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()


def test_get_enrolments_success():
    enrolment_filters = test_data.sample_enrolment_filters.dict()
    repo = mock.Mock(spec=EnrolmentRepo)
    use_case = GetEnrolments(enrolment_repo=repo)
    repo.get_enrolments.return_value = test_data.sample_result
    response = use_case.execute(enrolment_filters)

    assert response.type == SuccessType.SUCCESS


def test_get_enrolments_failure():
    enrolment_filters = test_data.sample_enrolment_filters.dict()
    repo = mock.Mock(spec=EnrolmentRepo)
    use_case = GetEnrolments(enrolment_repo=repo)

    repo.get_enrolments.side_effect = Exception()
    response = use_case.execute(enrolment_filters)

    assert response.type == FailureType.RESOURCE_ERROR
