"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
import datetime
from unittest.mock import patch
from uuid import UUID

from app.config import settings
from app.repositories.s3_course_repo import S3CourseRepo


@patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3Enrolmentrepo makes a boto3 connection.
    """
    S3CourseRepo()
    boto_client.assert_called_once()


@patch("uuid.uuid4")
@patch("boto3.client")
def test_save_course(boto_client, uuid4):
    """
    Ensure the S3Enrolmentrepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    course_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
    created = str(datetime.datetime.now())
    uuid4.return_value = UUID(course_id)
    repo = S3CourseRepo()
    settings.COURSE_BUCKET = "some-bucket"

    params = {
        "course_id": course_id,
        "course_name": "Bachelor of Community Services (HE20528)",
        "industry_standards": "Police Check",
        "competancy": "top rated",
        "location": "Sydney",
        "date": "2020-10-11T16:06:53.739338",
        "availablity": "morning",
        "hours_per_week": "10",
        "duration": "2 months",
        "fees_from": "200",
        "created": created,
    }
    course = repo.save_course(input_course=params)

    assert course_id == course.course_id
    assert "Bachelor of Community Services (HE20528)" == course.course_name
    assert "Police Check" == course.industry_standards
    assert "top rated" == course.competancy
    assert "Sydney" == course.location
    assert "2020-10-11T16:06:53.739338" == course.date
    assert "morning" == course.availablity
    assert "10" == course.hours_per_week
    assert "2 months" == course.duration
    assert "200" == course.fees_from
    assert created == course.created

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(course.json(), "utf-8"),
        Key=f"courses/{course_id}.json",  # NOQA
        Bucket="some-bucket",
    )