import uuid
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.enrolment_authorisation import EnrolmentAuthorisation
from app.repositories.enrolment_repo import EnrolmentRepo


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3 = boto3.client("s3", **settings.s3_configuration)

    def save_enrolment(self, course_id, student_id):
        # Create a submission uuid
        enrolment = EnrolmentAuthorisation(
            uuid=uuid.uuid4(), course_id=course_id, student_id=student_id
        )

        # Write directory to bucket
        self.s3.put_object(
            Body=bytes(enrolment.json(), "utf-8"),
            Key=f"{enrolment.uuid}.json",
            Bucket=settings.ENROLMENT_AUTHORISATION_BUCKET,
        )

        return enrolment
