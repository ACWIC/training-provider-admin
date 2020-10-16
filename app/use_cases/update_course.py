from pydantic import BaseModel

from app.repositories.course_repo import CourseRepo
from app.requests.update_course_request import UpdateCourseRequest
from app.responses import ResponseFailure, ResponseSuccess


class UpdateCourse(BaseModel):
    course_repo: CourseRepo

    class Config:
        # Pydantic will complain if something (enrolment_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, request: UpdateCourseRequest):

        print("request", request)
        params = {
            "course_id": request.course_id,
            "course_name": request.course_name,
            "industry_standards": request.industry_standards,
            "competancy": request.competancy,
            "location": request.location,
            "date": request.date,
            "availablity": request.availablity,
            "hours_per_week": request.hours_per_week,
            "duration": request.duration,
            "fees_from": request.fees_from,
        }

        try:
            course = self.course_repo.update_course(params)
        except Exception as e:  # noqa - TODO: handle specific failure types
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=course)
