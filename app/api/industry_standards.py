from fastapi import APIRouter, HTTPException

from app.repositories.s3_industry_standard_repo import S3IndustryStandardRepo
from app.requests.industry_standard_request import IndustryStandardRequest
from app.use_cases import delete_industry_standard as dis
from app.use_cases import get_industry_standards as gis
from app.use_cases import post_industry_standard as pis

router = APIRouter()
industry_standard_repo = S3IndustryStandardRepo()


@router.post("/industry_standards")
def post_industry_standard(inputs: IndustryStandardRequest):
    """Create a new industry_standard in industry_standard repository"""
    use_case = pis.PostIndustryStandard(industry_standard_repo=industry_standard_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.delete("/industry_standards/{standard_id}")
def delete_industry_standard(standard_id: str):
    """Delete an existing industry_standard in industry_standard respository"""
    use_case = dis.DeleteIndustryStandard(industry_standard_repo=industry_standard_repo)
    response = use_case.execute(standard_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.get("/industry_standards")
def get_industry_standards():
    """Get industry_standards list in industry_standard respository"""
    use_case = gis.GetIndustryStandards(industry_standard_repo=industry_standard_repo)
    response = use_case.execute()
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()
