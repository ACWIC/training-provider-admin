from unittest import mock

from botocore.stub import Stubber

from app.config import settings
from app.domain.entities.enrolment_request import EnrolmentAuth, State
from app.repositories.s3_enrolment_repo import (
    S3EnrolmentRepo,
    filters_match,
    if_dates_in_range,
    state_change_valid,
)
from tests.test_data.boto_client_responses import (
    get_object_response,
    list_objects_response,
    put_object_response,
)
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()


@mock.patch("json.loads")
def test_get_enrolments(json_loads):
    filters = test_data.sample_enrolment_auth_filters
    repo = S3EnrolmentRepo()
    stubber = Stubber(repo.s3)
    settings.ENROLMENT_AUTHORISATION_BUCKET = "some-bucket"
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
        get_object_response(test_data.sample_enrolment_auth),
        {
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.enrolment_id}.json",
        },
    )

    stubber.add_response(
        "get_object",
        get_object_response(test_data.sample_enrolment_auth1),
        {
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.enrolment_id1}.json",
        },
    )

    with stubber:
        results = repo.get_enrolments(filters)

    assert results == sample_result


@mock.patch("json.loads")
def test_get_enrolments_filter_by_date(json_loads):
    filters = test_data.sample_enrolment_auth_filters_2
    repo = S3EnrolmentRepo()
    stubber = Stubber(repo.s3)
    settings.ENROLMENT_AUTHORISATION_BUCKET = "some-bucket"
    sample_result = test_data.sample_result_2["enrolments"]
    json_loads.side_effect = [
        sample_result[0].dict(),
        sample_result[1].dict(),
    ]

    stubber.add_response(
        "list_objects",
        list_objects_response([test_data.enrolment_id1, test_data.enrolment_id2]),
        {"Bucket": "some-bucket"},
    )
    stubber.add_response(
        "get_object",
        get_object_response(test_data.sample_enrolment_auth),
        {
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.enrolment_id1}.json",
        },
    )

    stubber.add_response(
        "get_object",
        get_object_response(test_data.sample_enrolment_auth1),
        {
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.enrolment_id2}.json",
        },
    )

    with stubber:
        results = repo.get_enrolments(filters)

    # Only the second enrolment matches the filter, so result should have one item
    assert len(results) == 1
    assert results[0] == sample_result[1]


@mock.patch("json.loads")
def test_get_enrolment_auth_by_id(json_loads):
    repo = S3EnrolmentRepo()
    stubber = Stubber(repo.s3)
    settings.ENROLMENT_AUTHORISATION_BUCKET = "some-bucket"
    json_loads.side_effect = [test_data.sample_enrolment_auth.dict()]
    stubber.add_response(
        "get_object",
        get_object_response(test_data.sample_enrolment_auth),
        {
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.enrolment_id1}.json",
        },
    )
    with stubber:
        result = repo.get_enrolment_auth_by_id(test_data.enrolment_id1)

    assert isinstance(result, EnrolmentAuth)
    assert result == test_data.sample_enrolment_auth


def test_enrolment_auth_exists_success():
    repo = S3EnrolmentRepo()
    stubber = Stubber(repo.s3)
    settings.ENROLMENT_AUTHORISATION_BUCKET = "some-bucket"
    stubber.add_response(
        "get_object",
        get_object_response(test_data.sample_enrolment_auth),
        {
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.enrolment_id1}.json",
        },
    )
    with stubber:
        result = repo.enrolment_auth_exists(test_data.enrolment_id1)

    assert result is True


def test_enrolment_auth_exists_failure():
    repo = S3EnrolmentRepo()
    stubber = Stubber(repo.s3)
    settings.ENROLMENT_AUTHORISATION_BUCKET = "some-bucket"
    stubber.add_client_error(
        "get_object",
        {
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.enrolment_id1}.json",
        },
    )
    with stubber:
        result = repo.enrolment_auth_exists(test_data.enrolment_id1)

    assert result is False


def test_update_enrolment_state():
    repo = S3EnrolmentRepo()
    stubber = Stubber(repo.s3)
    settings.ENROLMENT_AUTHORISATION_BUCKET = "some-bucket"

    stubber.add_response(
        "put_object",
        put_object_response(),
        {
            "Body": bytes(test_data.updated_enrolment.json(), "utf-8"),
            "Bucket": "some-bucket",
            "Key": f"enrolment_authorisations/{test_data.updated_enrolment.enrolment_id}.json",
        },
    )
    with stubber:
        result = repo.update_enrolment_state(
            test_data.sample_enrolment_auth, State.ACCEPTED
        )

    assert isinstance(result, EnrolmentAuth)
    assert result.state == State.ACCEPTED


def test_filters_match():
    enrolment = test_data.sample_enrolment_auth.dict()
    enrolment_filters = test_data.sample_enrolment_auth_filters.dict()
    enrolment_filters1 = test_data.sample_enrolment_auth_filters_2.dict()

    assert filters_match(enrolment, enrolment_filters)
    assert not filters_match(enrolment, enrolment_filters1)


def test_if_dates_in_range():
    enrolment = test_data.enrolment_created_in_range
    enrolment_filters = test_data.enrolment_filters_start_date_in_range
    assert if_dates_in_range(enrolment, enrolment_filters)

    enrolment = test_data.enrolment_created_in_range
    enrolment_filters = test_data.enrolment_filters_received_date
    assert if_dates_in_range(enrolment, enrolment_filters)

    enrolment_filters = test_data.enrolment_filters_start_date_none
    assert if_dates_in_range(enrolment, enrolment_filters)

    # If there is nothing to filter, than this should return True
    enrolment_filters = {}
    assert if_dates_in_range(enrolment, enrolment_filters)

    enrolment = test_data.enrolment_created_not_in_range
    enrolment_filters = test_data.enrolment_filters_start_date_in_range
    assert not if_dates_in_range(enrolment, enrolment_filters)


def test_state_change_valid():
    assert state_change_valid(State.NEW, State.ACCEPTED)
    assert not state_change_valid(State.NEW, State.NEW)
    assert not state_change_valid(State.REJECTED, State.ACCEPTED)
