"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.industry_standard_repo import IndustryStandardRepo
from app.responses import FailureType, SuccessType
from app.use_cases.get_industry_standards import GetIndustryStandards
from tests.test_data.standards_data_provider import StandardsDataProvider

test_data = StandardsDataProvider()


def test_get_standard_success():
    """
    When getting standards,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=IndustryStandardRepo)
    use_case = GetIndustryStandards(industry_standard_repo=repo)

    repo.get_standards.return_value = test_data.industry_standard_list
    response = use_case.execute()

    assert response.type == SuccessType.SUCCESS


def test_get_standard_failure():
    """
    When getting standards,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=IndustryStandardRepo)
    repo.get_standards.side_effect = Exception()

    use_case = GetIndustryStandards(industry_standard_repo=repo)
    response = use_case.execute()

    assert response.type == FailureType.RESOURCE_ERROR
