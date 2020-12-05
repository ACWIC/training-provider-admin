from app.domain.entities.enrolment_request import EnrolmentAuth, EnrolmentAuthFilters
from tests.test_data.enrolment_data_provider import EnrolmentDataProvider

test_data = EnrolmentDataProvider()


def test_enrolment_init():
    enrolment = EnrolmentAuth(
        enrolment_auth_id=test_data.enrolment_auth_id,
        student_id=test_data.student_id,
        course_id=test_data.course_id,
        status=test_data.status,
        enrolment_id=test_data.enrolment_id,
        shared_secret=test_data.shared_secret,
        created=test_data.created,
        state=test_data.state,
    )

    assert enrolment.enrolment_auth_id == test_data.enrolment_auth_id
    assert enrolment.student_id == test_data.student_id
    assert enrolment.course_id == test_data.course_id
    assert enrolment.status == test_data.status
    assert enrolment.enrolment_id == test_data.enrolment_id
    assert enrolment.shared_secret == test_data.shared_secret
    assert enrolment.created == test_data.created
    assert enrolment.state == test_data.state


def test_enrolment_filters_init():
    enrolment_filters = EnrolmentAuthFilters(
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
