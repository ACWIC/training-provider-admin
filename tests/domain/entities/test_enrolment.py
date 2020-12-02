from app.domain.entities.enrolment_request import EnrolmentFilters, EnrolmentRequest
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()


def test_enrolment_init():
    enrolment = EnrolmentRequest(
        enrolment_id=test_data.enrolment_id,
        shared_secret=test_data.shared_secret,
        internal_reference=test_data.internal_reference,
        created=test_data.created,
        state=test_data.state,
    )

    assert enrolment.enrolment_id == test_data.enrolment_id
    assert enrolment.shared_secret == test_data.shared_secret
    assert enrolment.internal_reference == test_data.internal_reference
    assert enrolment.created == test_data.created
    assert enrolment.state == test_data.state


def test_enrolment_filters_init():
    enrolment_filters = EnrolmentFilters(
        course_id=test_data.course_id,
        start_date=test_data.start_date,
        end_date=test_data.end_date,
        receive_date=test_data.created,
        state=[test_data.state],
    )

    assert enrolment_filters.course_id == test_data.course_id
    assert enrolment_filters.start_date == test_data.start_date
    assert enrolment_filters.end_date == test_data.end_date
    assert enrolment_filters.receive_date == test_data.created
    assert enrolment_filters.state == [test_data.state]
