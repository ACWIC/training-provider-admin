from pydantic import BaseModel

from app.repositories.course_repo import CourseRepo
from app.requests.create_course_request import NewCourseRequest
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class CreateNewCourse(BaseModel):
    course_repo: CourseRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, create_course_request: NewCourseRequest):
        try:
            course = self.course_repo.create_course(create_course_request)
            code = SuccessType.CREATED
            message = "The course has been created."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=course, message=message, type=code)
