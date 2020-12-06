from fastapi import APIRouter, Depends, HTTPException

from app.repositories.s3_course_repo import S3CourseRepo
from app.requests.create_course_request import NewCourseRequest
from app.requests.update_course_request import UpdateCourseRequest
from app.security import oauth2_scheme
from app.use_cases import create_course as cc
from app.use_cases import get_course as gc
from app.use_cases import update_course as uc

router = APIRouter()
course_repo = S3CourseRepo()


@router.post("/course")
def post_course(inputs: NewCourseRequest, token: str = Depends(oauth2_scheme)):
    """Create a new Course in Course Catalogue"""
    use_case = cc.CreateNewCourse(course_repo=course_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)
    return response.build()


@router.put("/course")
def update_course(inputs: UpdateCourseRequest, token: str = Depends(oauth2_scheme)):
    """Update an existing Course in Course Catalogue
    course id is mandatory, other attributes are optional
    """
    use_case = uc.UpdateCourse(course_repo=course_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()


@router.get("/course/{course_id}")
def get_course(course_id: str, token: str = Depends(oauth2_scheme)):
    """Get an existing Course in Course Catalogue
    using course id
    """
    use_case = gc.GetCourseByID(course_repo=course_repo)
    response = use_case.execute(course_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()
