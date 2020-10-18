import datetime

from pydantic import BaseModel

from app.repositories.course_repo import CourseRepo
from app.requests.create_course_request import NewCourseRequest
from app.responses import ResponseFailure, ResponseSuccess
from app.utils import Random


class CreateNewCourse(BaseModel):
    course_repo: CourseRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, create_course_request: NewCourseRequest):
        input_course = vars(create_course_request)  # to dict
        input_course["course_id"] = str(Random.get_uuid())
        input_course["created"] = datetime.datetime.now()

        try:
            course = self.course_repo.create_course(input_course=input_course)
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=course)
