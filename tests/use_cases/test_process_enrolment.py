"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import FailureType, SuccessType
from app.use_cases.process_enrolments import ProcessEnrolmentAuths
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()


def test_process_enrolments_success():
    repo = mock.Mock(spec=EnrolmentRepo)
    enrolment = test_data.sample_enrolment_auth
    use_case = ProcessEnrolmentAuths(enrolment_repo=repo)
    repo.enrolment_auth_exists.return_value = True
    repo.get_enrolment_auth_by_id.return_value = enrolment
    response = use_case.execute(test_data.process_enrolment_request)

    assert response.type == SuccessType.SUCCESS


def test_process_enrolments_not_exists():
    repo = mock.Mock(spec=EnrolmentRepo)
    repo.enrolment_auth_exists.return_value = False

    use_case = ProcessEnrolmentAuths(enrolment_repo=repo)
    response = use_case.execute(test_data.process_enrolment_request)

    assert response.type == FailureType.VALIDATION_ERROR


def test_process_enrolments_state_change_not_valid():
    repo = mock.Mock(spec=EnrolmentRepo)
    enrolment = test_data.sample_enrolment_auth
    use_case = ProcessEnrolmentAuths(enrolment_repo=repo)
    repo.enrolment_auth_exists.return_value = True
    repo.get_enrolment_auth_by_id.return_value = enrolment
    response = use_case.execute(test_data.process_enrolment_failing_request)

    assert response.type == FailureType.VALIDATION_ERROR


def test_process_enrolments_failure():
    enrolment_filters = test_data.sample_enrolment_auth_filters.dict()
    repo = mock.Mock(spec=EnrolmentRepo)
    use_case = ProcessEnrolmentAuths(enrolment_repo=repo)

    repo.enrolment_auth_exists.return_value = True
    repo.get_enrolment_auth_by_id.side_effect = Exception()
    response = use_case.execute(enrolment_filters)

    assert response.type == FailureType.RESOURCE_ERROR
