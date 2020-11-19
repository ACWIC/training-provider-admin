from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.security import oauth2_scheme
from app.use_cases import process_enrolments as pe

router = APIRouter()
enrolment_repo = S3EnrolmentRepo()


@router.get("/enrolments")
def get_enrolment(
    course_id: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
    receive_date: Optional[str],
    token: str = Depends(oauth2_scheme),
):
    """Get enrolments by filtering"""
    inputs = {
        "course_id": course_id,
        "start_date": start_date,
        "end_date": end_date,
        "receive_date": receive_date,
    }
    use_case = pe.ProcessEnrolments(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()
