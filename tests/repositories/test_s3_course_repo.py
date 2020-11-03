"""
These tests evaluate the interaction with the backing PaaS.
The are testing the encapsulation of the "impure" code
(in a functional sense),
the repos should return pure domain objects
of the appropriate type.
"""
import datetime
from unittest import mock

from app.config import settings
from app.repositories.s3_course_repo import S3CourseRepo
from tests.test_data.course_data_provider import CourseDataProvider

test_data = CourseDataProvider()


@mock.patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3CourseRepo makes a boto3 connection.
    """
    S3CourseRepo()
    boto_client.assert_called_once()


@mock.patch("app.utils.random.Random.get_uuid")
@mock.patch("boto3.client")
def test_save_course(boto_client, get_uuid):
    repo = S3CourseRepo()
    settings.COURSE_BUCKET = "some-bucket"
    course_id = test_data.sample_course_id
    request = test_data.sample_create_course_request

    get_uuid.return_value = test_data.sample_course_id
    with mock_datetime_now(test_data.created, datetime):
        course = repo.create_course(request)

    print(course, test_data.sample_course)
    assert course == test_data.sample_course

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(course.json(), "utf-8"),
        Key=f"courses/{course_id}.json",  # NOQA
        Bucket="some-bucket",
    )


@mock.patch("app.repositories.s3_course_repo.S3CourseRepo.get_course")
@mock.patch("boto3.client")
def test_update_course(boto_client, repo_get_course):
    course_id = test_data.sample_course_id
    repo = S3CourseRepo()
    settings.COURSE_BUCKET = "some-bucket"
    sample_course = test_data.sample_course
    params = test_data.sample_update_course_request

    repo_get_course.return_value = sample_course
    course = repo.update_course(params)

    assert course == sample_course

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(course.json(), "utf-8"),
        Key=f"courses/{course_id}.json",  # NOQA
        Bucket="some-bucket",
    )


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_course(boto_client, json_loads):
    course_id = test_data.sample_course_id
    repo = S3CourseRepo()
    settings.COURSE_BUCKET = "some-bucket"
    sample_course = test_data.sample_course

    json_loads.return_value = sample_course.dict()
    course = repo.get_course(course_id)

    assert course == sample_course

    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"courses/{course_id}.json",
        Bucket="some-bucket",
    )


def mock_datetime_now(target, datetime_module):
    """Override ``datetime.datetime.now()`` with a custom target value.
    This creates a new datetime.datetime class, and alters its now()/utcnow()
    methods.
    Returns:
        A mock.mock.mock.patch context, can be used as a decorator or in a with.
    """
    real_datetime_class = datetime.datetime

    class DatetimeSubclassMeta(type):
        """We need to customize the __instancecheck__ method for isinstance().
        This must be performed at a metaclass level.
        """

        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

    # Python2 & Python3-compatible metaclass
    MockedDatetime = DatetimeSubclassMeta("datetime", (BaseMockedDatetime,), {})

    return mock.patch.object(datetime_module, "datetime", MockedDatetime)
