import datetime

from app.domain.entities.enrolment_request import (
    EnrolmentAuth,
    EnrolmentAuthFilters,
    State,
)
from app.requests.enrolment_requests import ProcessEnrolmentRequest


class EnrolmentDataProvider:
    sample_enrolment_auth: EnrolmentAuth

    enrolment_auth_id = "2dad3dd8-af28-4e61-ae23-4c93a456d10e"
    status = "Lodged"
    student_id = "4dad3dd8-af28-4e61-ae23-4c93a456d10e"
    enrolment_id = "2dad3dd8-af28-4e61-ae23-4c93a456d10e"
    enrolment_id1 = "3dad3dd8-af28-4e61-ae23-4c93a456d10f"
    enrolment_id2 = "4dad3dd8-af28-4e61-ae23-4c93a456d10f"
    shared_secret = "6dad3dd8-af28-4e61-ae23-4c93a456d10e"
    course_id = "7dad3dd8-af28-4e61-ae23-4c93a456d10e"
    date_time_str = "2018-05-29 08:15:27.243860"
    date_time_str1 = "2018-06-29 08:15:27.243860"
    date_time_str2 = "2018-07-29 08:15:27.243860"
    start_date = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
    end_date = datetime.datetime.strptime(date_time_str2, "%Y-%m-%d %H:%M:%S.%f")
    created = datetime.datetime.strptime(date_time_str1, "%Y-%m-%d %H:%M:%S.%f")
    state = State.NEW

    def __init__(self):
        self.sample_enrolment_auth = EnrolmentAuth(
            enrolment_auth_id=self.enrolment_auth_id,
            student_id=self.student_id,
            course_id=self.course_id,
            status=self.status,
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            created=self.created,
            state=self.state,
        )

        self.updated_enrolment = self.sample_enrolment_auth.dict()
        self.updated_enrolment["state"] = State.ACCEPTED
        self.updated_enrolment = EnrolmentAuth(**self.updated_enrolment)

        self.sample_enrolment_auth1 = EnrolmentAuth(
            enrolment_auth_id=self.enrolment_auth_id,
            student_id=self.student_id,
            course_id=self.course_id,
            status=self.status,
            enrolment_id=self.enrolment_id1,
            shared_secret=self.shared_secret,
            created=self.created,
            state=self.state,
        )

        self.sample_enrolment_auth2 = EnrolmentAuth(
            enrolment_auth_id=self.enrolment_auth_id,
            student_id=self.student_id,
            course_id=self.course_id,
            status=self.status,
            enrolment_id=self.enrolment_id2,
            shared_secret=self.shared_secret,
            created=self.start_date,
            state=self.state,
        )

        self.sample_enrolment_auth_filters = EnrolmentAuthFilters(
            course_id=self.course_id,
            start_date=self.start_date,
            end_date=self.end_date,
            receive_date=self.created,
        )

        self.sample_enrolment_auth_filters_json = {
            "course_id": self.course_id,
            "start_date": self.date_time_str,
            "end_date": self.date_time_str2,
            "receive_date": self.date_time_str1,
        }

        self.sample_enrolment_auth_filters_2 = EnrolmentAuthFilters(
            course_id=self.course_id,
            start_date=self.start_date,
            end_date=self.start_date,
        )

        self.sample_result = {
            "enrolments": [self.sample_enrolment_auth, self.sample_enrolment_auth1]
        }

        self.sample_result_2 = {
            "enrolments": [self.sample_enrolment_auth1, self.sample_enrolment_auth2]
        }

        self.process_enrolment_request = ProcessEnrolmentRequest(
            enrolment_request_id=self.enrolment_id, new_state=State.ACCEPTED
        )
        self.process_enrolment_failing_request = ProcessEnrolmentRequest(
            enrolment_request_id=self.enrolment_id, new_state=State.CANCELLED
        )

        # start date
        self.enrolment_created_in_range = {
            "created": datetime.datetime.strptime(
                "2018-06-05 08:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"
            ),
        }
        self.enrolment_created_not_in_range = {
            "created": datetime.datetime.strptime(
                "2018-06-15 08:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"
            ),
        }
        self.enrolment_filters_start_date_in_range = {
            "start_date": datetime.datetime.strptime(
                "2018-06-01 08:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"
            ),
            "end_date": datetime.datetime.strptime(
                "2018-06-10 08:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"
            ),
            "receive_date": None,
        }
        self.enrolment_filters_start_date_none = {
            "start_date": None,
            "end_date": None,
            "receive_date": None,
        }

        self.enrolment_filters_received_date = {
            "start_date": None,
            "end_date": None,
            "receive_date": datetime.datetime.strptime(
                "2018-06-05 15:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"
            ),
        }
