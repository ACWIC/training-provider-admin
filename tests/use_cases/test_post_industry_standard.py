"""
These tests evaluate (and document) the business logic.
"""
from unittest import mock

from app.repositories.industry_standard_repo import IndustryStandardRepo
from app.responses import FailureType, SuccessType
from app.use_cases.post_industry_standard import PostIndustryStandard
from tests.test_data.standards_data_provider import StandardsDataProvider

test_data = StandardsDataProvider()


def test_post_standard_success():
    """
    When posting a standard,
    if everything goes according to plan,
    the response type should be "Success".
    """
    repo = mock.Mock(spec=IndustryStandardRepo)
    use_case = PostIndustryStandard(industry_standard_repo=repo)

    repo.post_industry_standard.return_value = test_data.industry_standard
    response = use_case.execute(test_data.industry_standard_request)

    assert response.type == SuccessType.CREATED


def test_post_standard_failure():
    """
    When posting a standard,
    if there is some kind of error,
    the response type should be "ResourceError".
    """
    repo = mock.Mock(spec=IndustryStandardRepo)
    repo.post_industry_standard.side_effect = Exception()

    use_case = PostIndustryStandard(industry_standard_repo=repo)
    response = use_case.execute(test_data.industry_standard_request)

    assert response.type == FailureType.RESOURCE_ERROR
