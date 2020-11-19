from pydantic import BaseModel

from app.domain.entities.enrolment import EnrolmentFilters
from app.repositories.course_repo import CourseRepo
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class ProcessEnrolments(BaseModel):
    enrolment_repo: EnrolmentRepo
    course_repo: CourseRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, enrolment_filters: dict):
        try:
            course_id = enrolment_filters["course_id"]
            # Check if course with course_id exists
            if not self.course_repo.course_exists(course_id):
                return ResponseFailure.build_from_validation_error(
                    message=f"Course_id={course_id} is invalid."
                )
            course = self.course_repo.get_course(course_id)
            enrolment_filters = EnrolmentFilters(**enrolment_filters)
            enrolments = self.enrolment_repo.get_enrolments(enrolment_filters)
            # TODO: add process stuff here, reject/accept each enrolment
            result = {"course": course, "enrolments": enrolments}
            code = SuccessType.SUCCESS
            message = "The enrolments have been processed."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=result, message=message, type=code)
