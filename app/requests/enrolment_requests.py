from app.requests import ValidRequest


class EnrolmentAuthRequest(ValidRequest):
    enrolment_request_id: str
    new_state: str
