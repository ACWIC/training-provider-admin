from pydantic import BaseModel

from app.domain.entities.enrolment_request import EnrolmentFilters
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class GetEnrolments(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, enrolment_filters: dict):
        try:
            enrolment_filters = EnrolmentFilters(**enrolment_filters)
            enrolments = self.enrolment_repo.get_enrolments(enrolment_filters)
            result = {"enrolments": enrolments}
            code = SuccessType.SUCCESS
            message = "The enrolments have been fetched."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=result, message=message, type=code)
