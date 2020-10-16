from uuid import uuid4

from app.requests.update_course_request import UpdateCourseRequest


def test_update_course_request():
    """
    When a NewEnrollmentRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    course_id = str(uuid4())
    request = UpdateCourseRequest(
        course_id=course_id,
        course_name="Bachelor of Community Services (HE20528)",
        industry_standards="Police Check",
        competancy="top rated",
        location="Sydney",
        date="2020-10-11T16:06:53.739338",
        availablity="morning",
        hours_per_week="10",
        duration="2 months",
        fees_from="200",
    )

    assert course_id == request.course_id
    assert "Bachelor of Community Services (HE20528)" == request.course_name
    assert "Police Check" == request.industry_standards
    assert "top rated" == request.competancy
    assert "Sydney" == request.location
    assert "2020-10-11T16:06:53.739338" == request.date
    assert "morning" == request.availablity
    assert "10" == request.hours_per_week
    assert "2 months" == request.duration
    assert "200" == request.fees_from
