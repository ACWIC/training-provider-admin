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
    """
    Create a new Course in Course Catalogue\n
    <b>course_name</b> is required.\n
    <b>industry_standards</b> is a list of industry standard versions
    this course confirms to.\n
    <b>competency</b> is a list of competencies.\n
    <b>location</b> is the location where course is conducted.
    It is required.\n
    <b>start_date</b> is in format ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ).
    It is the starting date of the course.
    It is required.\n
    <b>availability</b> is a boolean which is True or False depending
    upon the availability of the course. It is required.\n
    <b>hours_per_week</b> is the number of hours per week the course
    demands from the students. It is a float value. It is required.\n
    <b>duration</b> is the total duration of course in string.
    It is required.\n
    <b>fees_from</b> is the minimum fee of the course.
    It is a float value. It is required\n
    """
    use_case = cc.CreateNewCourse(course_repo=course_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()


@router.put("/course")
def update_course(inputs: UpdateCourseRequest, token: str = Depends(oauth2_scheme)):
    """Update an existing Course in Course Catalogue\n
    <b>course_id</b> is mandatory which identifies the course.\n
    <b>course_name</b> is optional.\n
    <b>industry_standards</b> is a list of industry standard versions
    this course confirms to. It is optional\n
    <b>competency</b> is a list of competencies. It is optional\n
    <b>location</b> is the location where course is conducted.
    It is optional.\n
    <b>start_date</b> is in format ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ).
    It is the starting date of the course.
    It is optional.\n
    <b>availability</b> is a boolean which is True or False depending
    upon the availability of the course. It is optional.\n
    <b>hours_per_week</b> is the number of hours per week the course
    demands from the students. It is a float value. It is optional.\n
    <b>duration</b> is the total duration of course in string.
    It is optional.\n
    <b>fees_from</b> is the minimum fee of the course.
    It is a float value. It is optional\n
    """
    use_case = uc.UpdateCourse(course_repo=course_repo)
    response = use_case.execute(inputs)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()


@router.get("/course/{course_id}")
def get_course(course_id: str, token: str = Depends(oauth2_scheme)):
    """Get an existing Course in Course Catalogue.\n
    This API returns the information of the course.\n
    <b>course_id</b> is mandatory which identifies the course.\n
    """
    use_case = gc.GetCourseByID(course_repo=course_repo)
    response = use_case.execute(course_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()
