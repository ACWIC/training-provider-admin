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
    **course_name** is required.\n
    **industry_standards** is a list of industry standard versions
    this course confirms to.\n
    **competency** is a list of competencies.\n
    **location** is the location where course is conducted.
    It is required.\n
    **start_date** is in format ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ).
    It is the starting date of the course.
    It is required.\n
    **availability** is a boolean which is True or False depending
    upon the availability of the course. It is required.\n
    **hours_per_week** is the number of hours per week the course
    demands from the students. It is a float value. It is required.\n
    **duration** is the total duration of course in string.
    It is required.\n
    **fees_from** is the minimum fee of the course.
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
    **course_id** is mandatory which identifies the course.\n
    **course_name** is optional.\n
    **industry_standards** is a list of industry standard versions
    this course confirms to. It is optional\n
    **competency** is a list of competencies. It is optional\n
    **location** is the location where course is conducted.
    It is optional.\n
    **start_date** is in format ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ).
    It is the starting date of the course.
    It is optional.\n
    **availability** is a boolean which is True or False depending
    upon the availability of the course. It is optional.\n
    **hours_per_week** is the number of hours per week the course
    demands from the students. It is a float value. It is optional.\n
    **duration** is the total duration of course in string.
    It is optional.\n
    **fees_from** is the minimum fee of the course.
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
    **course_id** is mandatory which identifies the course.\n
    """
    use_case = gc.GetCourseByID(course_repo=course_repo)
    response = use_case.execute(course_id)
    if bool(response) is False:  # If request failed
        raise HTTPException(status_code=response.type.value, detail=response.message)

    return response.build()
