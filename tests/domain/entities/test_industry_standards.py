from app.domain.entities.industry_standard import IndustryStandard
from tests.test_data.standards_data_provider import StandardsDataProvider

test_data = StandardsDataProvider()


def test_industry_standard_init():
    """
    Ensure the industry_standard data matches constructor values
    """
    industry_standard = IndustryStandard(
        standard_id=test_data.standard_id,
        standard_title=test_data.standard_title,
        standard_version=test_data.standard_version,
        standard_status=test_data.standard_status,
        status_attained_date=test_data.status_attained_date,
        review_date=test_data.review_date,
        competencies_list=test_data.competencies_list,
    )

    assert industry_standard.standard_id == test_data.standard_id
    assert industry_standard.standard_title == test_data.standard_title
    assert industry_standard.standard_version == test_data.standard_version
    assert industry_standard.standard_status == test_data.standard_status
    assert industry_standard.status_attained_date == test_data.status_attained_date
    assert industry_standard.review_date == test_data.review_date
    assert industry_standard.competencies_list == test_data.competencies_list
