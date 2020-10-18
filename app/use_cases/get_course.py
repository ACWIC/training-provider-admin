from pydantic import BaseModel

from app.repositories.course_repo import CourseRepo
from app.responses import ResponseFailure, ResponseSuccess


class GetCourseByID(BaseModel):
    course_repo: CourseRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, course_id: str):
        try:
            course_id = self.course_repo.get_course(course_id=course_id)
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=course_id)
