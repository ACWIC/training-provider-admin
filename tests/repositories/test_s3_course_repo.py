"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
from unittest.mock import patch

from app.config import settings
from app.repositories.s3_course_repo import S3CourseRepo
from tests.test_data.course_data_provider import CourseDataProvider


@patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3CourseRepo makes a boto3 connection.
    """
    S3CourseRepo()
    boto_client.assert_called_once()


@patch("boto3.client")
def test_save_course(boto_client):
    """
    Ensure the S3CourseRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    course_id = CourseDataProvider().sample_course_id
    date = CourseDataProvider().sample_course_date
    repo = S3CourseRepo()
    settings.COURSE_BUCKET = "some-bucket"
    params = CourseDataProvider().sample_course_dict

    course = repo.create_course(input_course=params)

    assert course.course_id == course_id
    assert course.course_name == "Bachelor of Community Services (HE20528)"
    assert course.industry_standards == "Police Check"
    assert course.competency == "top rated"
    assert course.location == "Sydney"
    assert course.date == date
    assert course.availability is True
    assert course.hours_per_week == 10
    assert course.duration == "2 months"
    assert course.fees_from == 200
    assert course.created == date

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(course.json(), "utf-8"),
        Key=f"courses/{course_id}.json",  # NOQA
        Bucket="some-bucket",
    )


@patch("app.repositories.s3_course_repo.S3CourseRepo.get_course")
@patch("boto3.client")
def test_update_course(boto_client, repo_get_course):
    """
    Ensure the S3CourseRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    course_id = CourseDataProvider().sample_course_id
    date = CourseDataProvider().sample_course_date
    repo = S3CourseRepo()
    settings.COURSE_BUCKET = "some-bucket"
    course = CourseDataProvider().sample_course
    params = CourseDataProvider().sample_update_course_request_dict

    repo_get_course.return_value = course
    course = repo.update_course(params)

    assert course.course_id == course_id
    assert course.course_name == "Bachelor of Community Services (HE20528)"
    assert course.industry_standards == "Police Check"
    assert course.competency == "top rated"
    assert course.location == "Sydney"
    assert course.date == date
    assert course.availability is True
    assert course.hours_per_week == 10
    assert course.duration == "2 months"
    assert course.fees_from == 200
    assert course.created == date

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(course.json(), "utf-8"),
        Key=f"courses/{course_id}.json",  # NOQA
        Bucket="some-bucket",
    )


@patch("json.loads")
@patch("boto3.client")
def test_get_course(boto_client, json_loads):
    """
    Ensure the S3CourseRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    course_id = CourseDataProvider().sample_course_id
    date = CourseDataProvider().sample_course_date
    repo = S3CourseRepo()
    settings.COURSE_BUCKET = "some-bucket"
    course = CourseDataProvider().sample_course_dict

    json_loads.return_value = course
    course = repo.get_course(course_id)

    assert course.course_id == course_id
    assert course.course_name == "Bachelor of Community Services (HE20528)"
    assert course.industry_standards == "Police Check"
    assert course.competency == "top rated"
    assert course.location == "Sydney"
    assert course.date == date
    assert course.availability is True
    assert course.hours_per_week == 10
    assert course.duration == "2 months"
    assert course.fees_from == 200
    assert course.created == date

    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"courses/{course_id}.json",
        Bucket="some-bucket",
    )
