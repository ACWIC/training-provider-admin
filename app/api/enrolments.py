from fastapi import APIRouter, Depends, HTTPException

from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.security import oauth2_scheme
from app.use_cases import create_new_enrolment as cne

router = APIRouter()
enrolment_repo = S3EnrolmentRepo()


@router.get("/enrolments/{enrolment_id}")
def enrolments(enrolment_id: str, token: str = Depends(oauth2_scheme)):
    """Getting an enrollment by ID will return the current
    state of the enrollment, derived from the enrollment’s journal.
    """
    return {"your_enrolment_id": enrolment_id}


@router.post("/enrolments")
def create_enrolment(inputs: NewEnrolmentRequest, token: str = Depends(oauth2_scheme)):
    """Posting an enrollment authorisation is a synchronous proccess that
    immediately succeeds (or fails) to create an enrollment authorisation,
    and assign it a unique enrollment authorisation id.

    The initial state of the enrollment authorisation is “lodged”.
    """
    use_case = cne.CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)

    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()
