from pydantic import BaseModel

from app.repositories.enrolment_repo import EnrolmentRepo
from app.repositories.s3_enrolment_repo import state_change_valid
from app.requests.enrolment_requests import ProcessEnrolmentRequest
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class ProcessEnrolmentAuths(BaseModel):
    enrolment_repo: EnrolmentRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, process_enrolment_request: ProcessEnrolmentRequest):
        try:
            new_state = process_enrolment_request.new_state
            enrolment_auth_id = process_enrolment_request.enrolment_request_id
            if not self.enrolment_repo.enrolment_auth_exists(enrolment_auth_id):
                return ResponseFailure.build_from_validation_error(
                    message=f"Enrolment_id={enrolment_auth_id} is invalid."
                )
            enrolment = self.enrolment_repo.get_enrolment_auth_by_id(enrolment_auth_id)
            current_state = enrolment.state
            if not state_change_valid(current_state, new_state=new_state):
                return ResponseFailure.build_from_validation_error(
                    message=f"You can't change enrolment's state from {current_state} to {new_state}."
                )

            self.enrolment_repo.update_enrolment_state(enrolment, new_state)
            code = SuccessType.SUCCESS
            message = "The enrolment's state has been changed."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=enrolment, message=message, type=code)
