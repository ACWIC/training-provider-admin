"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.industry_standard_repo import IndustryStandardRepo
from app.responses import FailureType, SuccessType
from app.use_cases.delete_industry_standard import DeleteIndustryStandard
from tests.test_data.standards_data_provider import StandardsDataProvider

test_data = StandardsDataProvider()


def test_delete_standard_success():
    """
    When deleting a standard,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=IndustryStandardRepo)
    standard_id = test_data.standard_id
    use_case = DeleteIndustryStandard(industry_standard_repo=repo)

    repo.delete_industry_standard.return_value = {}
    response = use_case.execute(standard_id)

    assert response.type == SuccessType.SUCCESS


def test_delete_standard_not_exists():
    repo = mock.Mock(spec=IndustryStandardRepo)
    standard_id = test_data.standard_id
    repo.standard_exists.return_value = False

    use_case = DeleteIndustryStandard(industry_standard_repo=repo)
    response = use_case.execute(standard_id)

    assert response.type == FailureType.VALIDATION_ERROR


def test_delete_standard_failure():
    """
    When deleting a standard,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=IndustryStandardRepo)
    standard_id = test_data.standard_id
    repo.delete_industry_standard.side_effect = Exception()

    use_case = DeleteIndustryStandard(industry_standard_repo=repo)
    response = use_case.execute(standard_id)

    assert response.type == FailureType.RESOURCE_ERROR
