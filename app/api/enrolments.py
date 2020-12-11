from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.domain.entities.enrolment_request import State
from app.repositories.s3_course_repo import S3CourseRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.enrolment_requests import ProcessEnrolmentRequest
from app.security import oauth2_scheme
from app.use_cases import get_enrolments as ge
from app.use_cases import process_enrolments as pe

router = APIRouter()
course_repo = S3CourseRepo()
enrolment_repo = S3EnrolmentRepo()


@router.get("/enrolment_requests")
def get_enrolment_requests(
    course_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    receive_date: Optional[str] = None,
    token: str = Depends(oauth2_scheme),
):
    """Get enrolment requests by filtering"""
    inputs = {
        "course_id": course_id,
        "start_date": start_date,
        "end_date": end_date,
        "receive_date": receive_date,
    }
    use_case = ge.GetEnrolmentAuths(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.patch("/enrolment_requests/{enrolment_request_id}")
def process_enrolment(
    enrolment_request_id: str,
    new_state: State,
    token: str = Depends(oauth2_scheme),
):
    """Change state of enrolment with the given new state value"""

    request = ProcessEnrolmentRequest(
        enrolment_request_id=enrolment_request_id,
        new_state=new_state,
    )
    use_case = pe.ProcessEnrolmentAuths(enrolment_repo=enrolment_repo)
    response = use_case.execute(request)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()
