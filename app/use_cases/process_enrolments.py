from pydantic import BaseModel

from app.domain.entities.enrolment import EnrolmentFilters
from app.repositories.enrolment_repo import EnrolmentRepo
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class ProcessEnrolments(BaseModel):
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
            # TODO: add process stuff here
            code = SuccessType.SUCCESS
            message = "The enrolments have been fetched."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolments, message=message, type=code)
