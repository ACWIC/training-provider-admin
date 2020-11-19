from unittest import mock

from botocore.stub import Stubber

from app.config import settings
from app.repositories.s3_enrolment_repo import S3EnrolmentRepo
from tests.test_data.boto_client_responses import (
    get_object_response,
    list_objects_response,
)
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()


@mock.patch("json.loads")
def test_get_enrolments(json_loads):
    filters = test_data.sample_enrolment_filters
    repo = S3EnrolmentRepo()
    stubber = Stubber(repo.s3)
    settings.ENROLMENT_BUCKET = "some-bucket"
    sample_result = test_data.sample_result["enrolments"]
    json_loads.side_effect = [
        sample_result[0].dict(),
        sample_result[1].dict(),
    ]

    stubber.add_response(
        "list_objects",
        list_objects_response([test_data.enrolment_id, test_data.enrolment_id1]),
        {"Bucket": "some-bucket"},
    )
    stubber.add_response(
        "get_object",
        get_object_response(test_data.sample_enrolment),
        {"Bucket": "some-bucket", "Key": f"enrolments/{test_data.enrolment_id}.json"},
    )

    stubber.add_response(
        "get_object",
        get_object_response(test_data.sample_enrolment1),
        {"Bucket": "some-bucket", "Key": f"enrolments/{test_data.enrolment_id1}.json"},
    )

    with stubber:
        results = repo.get_enrolments(filters)

    assert results == sample_result
