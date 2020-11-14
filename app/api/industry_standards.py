from fastapi import APIRouter

from app.repositories.s3_industry_standard_repo import S3IndustryStandardRepo
from app.requests.industry_standard_request import NewIndustryStandard
from app.use_cases.delete_industry_standard import DeleteIndustryStandard
from app.use_cases.get_industry_standards import GetIndustryStandards
from app.use_cases.post_industry_standard import PostIndustryStandard

router = APIRouter()
industry_standard_repo = S3IndustryStandardRepo()


@router.post("/industry_standard")
def post_industry_standard(inputs: NewIndustryStandard):
    """Create a new industry_standard in industry_standard repository"""
    use_case = PostIndustryStandard(industry_standard_repo=industry_standard_repo)
    response = use_case.execute(inputs)
    return response


@router.delete("/industry_standard/{standard_id}")
def delete_industry_standard(standard_id: str):
    """Delete an existing industry_standard in industry_standard respository"""
    use_case = DeleteIndustryStandard(industry_standard_repo=industry_standard_repo)
    response = use_case.execute(standard_id)
    return response


@router.get("/industry_standards")
def get_industry_standards():
    """Get industry_standards list in industry_standard respository"""
    use_case = GetIndustryStandards(industry_standard_repo=industry_standard_repo)
    response = use_case.execute()
    return response
