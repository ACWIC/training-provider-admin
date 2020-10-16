from fastapi import APIRouter

from app.repositories.s3_course_repo import S3CourseRepo
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from app.requests.create_course_request import NewCourseRequest
from app.requests.enrolment_requests import NewEnrolmentRequest
from app.requests.update_course_request import UpdateCourseRequest
from app.use_cases.create_course import CreateNewCourse
from app.use_cases.create_new_enrolment import CreateNewEnrolment
from app.use_cases.update_course import UpdateCourse

router = APIRouter()
course_repo = S3CourseRepo()
enrolment_repo = S3EnrolmentRepo()


@router.post("/post_course")
def post_course(inputs: NewCourseRequest):
    """
    The Employer pre-registers a new Enrolment so callbacks can be received
    The assumption is that the employer generates a unique *enrolment_id*
    in some source system they control (LMS, HRMS, etc),
    and registers it with this microservice.
    This allows the microservice to generate keys,
    and prepare to receive callbacks from the training provider
    about this enrolment.
    """
    use_case = CreateNewCourse(course_repo=course_repo)
    response = use_case.execute(inputs)
    return response


@router.post("/update_course")
def update_course(inputs: UpdateCourseRequest):
    """
    The Employer pre-registers a new Enrolment so callbacks can be received
    The assumption is that the employer generates a unique *enrolment_id*
    in some source system they control (LMS, HRMS, etc),
    and registers it with this microservice.
    This allows the microservice to generate keys,
    and prepare to receive callbacks from the training provider
    about this enrolment.
    """
    use_case = UpdateCourse(course_repo=course_repo)
    response = use_case.execute(inputs)
    return response


@router.get("/enrolments/{enrolment_id}")
def enrolments(enrolment_id: str):
    """Getting an enrollment by ID will return the current
    state of the enrollment, derived from the enrollment’s journal.
    """
    return {"your_enrolment_id": enrolment_id}


@router.post("/enrolments")
def create_enrolment(inputs: NewEnrolmentRequest):
    """Posting an enrollment authorisation is a synchronous proccess that
    immediately succeeds (or fails) to create an enrollment authorisation,
    and assign it a unique enrollment authorisation id.

    The initial state of the enrollment authorisation is “lodged”.
    """
    use_case = CreateNewEnrolment(enrolment_repo=enrolment_repo)
    response = use_case.execute(inputs)

    return response
