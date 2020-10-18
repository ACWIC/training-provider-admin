from pydantic import BaseModel

from app.repositories.course_repo import CourseRepo
from app.requests.update_course_request import UpdateCourseRequest
from app.responses import ResponseFailure, ResponseSuccess


class UpdateCourse(BaseModel):
    course_repo: CourseRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, update_course_request: UpdateCourseRequest):
        new_course = vars(update_course_request)  # to dict
        try:
            course = self.course_repo.update_course(new_course=new_course)
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=course)
