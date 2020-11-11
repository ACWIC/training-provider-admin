from pydantic import BaseModel

from app.repositories.course_repo import CourseRepo
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class GetCourseByID(BaseModel):
    course_repo: CourseRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, course_id: str):
        try:
            # Check if course with course_id exists
            if not self.course_repo.course_exists(course_id):
                return ResponseFailure.build_from_validation_error(
                    message=f"Course_id={course_id} is invalid."
                )
            course = self.course_repo.get_course(course_id=course_id)
            code = SuccessType.SUCCESS
            message = "The course has been fetched."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=course, message=message, type=code)
