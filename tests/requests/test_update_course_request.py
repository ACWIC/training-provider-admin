import datetime
from uuid import uuid4

from app.requests.update_course_request import UpdateCourseRequest


def test_update_course_request():
    """
    When a UpdateCourseRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    course_id = str(uuid4())
    date = datetime.datetime.now()
    request = UpdateCourseRequest(
        course_id=course_id,
        course_name="Bachelor of Community Services (HE20528)",
        industry_standards="Police Check",
        competency="top rated",
        location="Sydney",
        date=date,
        availability=True,
        hours_per_week=10,
        duration="2 months",
        fees_from=200,
    )

    assert course_id == request.course_id
    assert request.course_name == "Bachelor of Community Services (HE20528)"
    assert request.industry_standards == "Police Check"
    assert request.competency == "top rated"
    assert request.location == "Sydney"
    assert request.date == date
    assert request.availability is True
    assert request.hours_per_week == 10
    assert request.duration == "2 months"
    assert request.fees_from == 200
