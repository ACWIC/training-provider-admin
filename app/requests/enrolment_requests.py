from app.requests import ValidRequest


class ProcessEnrolmentRequest(ValidRequest):
    enrolment_request_id: str
    new_state: str
