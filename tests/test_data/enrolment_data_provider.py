import datetime

from app.domain.entities.enrolment import Enrolment, EnrolmentFilters
from app.utils.random import Random


class EnrolmentDataProvider:
    sample_enrolment: Enrolment

    internal_reference = "ref1"
    ref_hash = Random.get_str_hash(internal_reference)
    sample_uuid = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    enrolment_id = "2dad3dd8-af28-4e61-ae23-4c93a456d10e"
    enrolment_id1 = "3dad3dd8-af28-4e61-ae23-4c93a456d10f"
    enrolment_id2 = "4dad3dd8-af28-4e61-ae23-4c93a456d10f"
    shared_secret = "6dad3dd8-af28-4e61-ae23-4c93a456d10e"
    course_id = "7dad3dd8-af28-4e61-ae23-4c93a456d10e"
    employee_id = "8dad3dd8-af28-4e61-ae23-4c93a456d10e"
    date_time_str = "2018-05-29 08:15:27.243860"
    date_time_str1 = "2018-06-29 08:15:27.243860"
    date_time_str2 = "2018-07-29 08:15:27.243860"
    start_date = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
    end_date = datetime.datetime.strptime(date_time_str2, "%Y-%m-%d %H:%M:%S.%f")
    received1 = datetime.datetime.strptime(date_time_str1, "%Y-%m-%d %H:%M:%S.%f")
    created = received1

    def __init__(self):
        self.sample_enrolment = Enrolment(
            enrolment_id=self.enrolment_id,
            shared_secret=self.shared_secret,
            internal_reference=self.ref_hash,
            created=self.created,
        )

        self.sample_create_enrolment = Enrolment(
            enrolment_id=self.sample_uuid,
            shared_secret=self.sample_uuid,
            internal_reference=self.ref_hash,
            created=self.created,
        )

        self.sample_enrolment1 = Enrolment(
            enrolment_id=self.enrolment_id1,
            shared_secret=self.shared_secret,
            internal_reference=self.ref_hash,
            created=self.created,
        )

        self.sample_enrolment2 = Enrolment(
            enrolment_id=self.enrolment_id2,
            shared_secret=self.shared_secret,
            internal_reference=self.ref_hash,
            created=self.start_date,
        )

        self.sample_enrolment_filters = EnrolmentFilters(
            course_id=self.course_id,
            start_date=self.start_date,
            end_date=self.end_date,
            receive_date=self.created,
        )

        self.sample_enrolment_filters_json = {
            "course_id": self.course_id,
            "start_date": self.date_time_str,
            "end_date": self.date_time_str2,
            "receive_date": self.date_time_str1,
        }

        self.sample_enrolment_filters_2 = EnrolmentFilters(
            course_id=self.course_id,
            start_date=self.start_date,
            end_date=self.start_date,
        )

        self.sample_result = {
            "enrolments": [self.sample_enrolment, self.sample_enrolment1]
        }

        self.sample_result_2 = {
            "enrolments": [self.sample_enrolment1, self.sample_enrolment2]
        }

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
            "receive_data": None,
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
