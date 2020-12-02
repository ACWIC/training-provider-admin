from app.requests.industry_standard_request import IndustryStandardRequest
from tests.test_data.standards_data_provider import StandardsDataProvider

test_data = StandardsDataProvider()


def test_industry_standard_request_init():
    """
    Ensure the industry_standard_request data matches constructor values
    """
    industry_standard_request = IndustryStandardRequest(
        standard_title=test_data.standard_title,
        standard_version=test_data.standard_version,
        standard_status=test_data.standard_status,
        status_attained_date=test_data.status_attained_date,
        review_date=test_data.review_date,
        competencies_list=test_data.competencies_list,
    )

    assert industry_standard_request.standard_title == test_data.standard_title
    assert industry_standard_request.standard_version == test_data.standard_version
    assert industry_standard_request.standard_status == test_data.standard_status
    assert (
        industry_standard_request.status_attained_date == test_data.status_attained_date
    )
    assert industry_standard_request.review_date == test_data.review_date
    assert industry_standard_request.competencies_list == test_data.competencies_list
