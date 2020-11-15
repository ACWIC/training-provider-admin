import datetime
from unittest import mock

from app.config import settings
from app.repositories.s3_industry_standard_repo import S3IndustryStandardRepo
from tests.test_data.standards_data_provider import StandardsDataProvider

test_data = StandardsDataProvider()


@mock.patch("boto3.client")
def test_s3_initialisation(boto_client):
    """
    Ensure the S3industry_standardRepo makes a boto3 connection.
    """
    S3IndustryStandardRepo()
    boto_client.assert_called_once()


@mock.patch("app.utils.random.Random.get_uuid")
@mock.patch("boto3.client")
def test_post_industry_standard(boto_client, get_uuid):
    repo = S3IndustryStandardRepo()
    settings.STANDARDS_BUCKET = "some-bucket"
    industry_standard_id = test_data.standard_id
    request = test_data.industry_standard_request

    get_uuid.return_value = test_data.standard_id
    industry_standard = repo.post_industry_standard(request)

    assert industry_standard == test_data.industry_standard

    boto_client.return_value.put_object.assert_called_once_with(
        Body=bytes(industry_standard.json(), "utf-8"),
        Key=f"industry_standards/{industry_standard_id}.json",  # NOQA
        Bucket="some-bucket",
    )


@mock.patch("boto3.client")
def test_delete_industry_standard(boto_client):
    repo = S3IndustryStandardRepo()
    settings.STANDARDS_BUCKET = "some-bucket"
    standard_id = test_data.standard_id

    repo.delete_industry_standard(standard_id)

    boto_client.return_value.delete_object.assert_called_once_with(
        Key=f"industry_standards/{standard_id}.json",
        Bucket="some-bucket",
    )


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_industry_standards(boto_client, json_loads):
    """
    Ensure the S3standardRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    repo = S3IndustryStandardRepo()
    settings.STANDARDS_BUCKET = "some-bucket"
    standard_id = test_data.standard_id

    industry_standard = test_data.industry_standard.dict()

    boto_client.return_value.list_objects = list_objects_sample_content
    json_loads.return_value = industry_standard
    standards_list = repo.get_standards()

    assert standards_list == {
        "standards_list": [{"standard": test_data.industry_standard.dict()}]
    }

    boto_client.return_value.get_object.assert_called_once_with(
        Key=f"industry_standards/{standard_id}.json",
        Bucket="some-bucket",
    )


@mock.patch("json.loads")
@mock.patch("boto3.client")
def test_get_standard_empty_list(boto_client, json_loads):
    """
    Ensure the S3standardRepo returns an object with OK data
    and that an appropriate boto3 put call was made.
    """
    repo = S3IndustryStandardRepo()
    settings.STANDARDS_BUCKET = "some-bucket"

    industry_standard = test_data.industry_standard.dict()

    boto_client.return_value.list_objects = list_objects_sample_content_empty
    json_loads.return_value = industry_standard
    standards_list = repo.get_standards()

    assert standards_list == {"standards_list": []}


def list_objects_sample_content(Bucket, Prefix):
    return {
        "Contents": [
            {
                "standard_id": test_data.standard_id,
                "bucket": Bucket,
                "prefix": Prefix,
                "Key": f"industry_standards/{test_data.standard_id}.json",
            }
        ]
    }


def list_objects_sample_content_empty(Bucket, Prefix):
    return {}


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
