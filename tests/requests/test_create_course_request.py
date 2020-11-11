import datetime

from app.requests.create_course_request import NewCourseRequest


def test_create_course_request():
    """
    When a NewCourseRequest is instantiated,
    the resulting object should have correct attribute values.
    """
    date = datetime.datetime.now()
    request = NewCourseRequest(
        course_name="Bachelor of Community Services (HE20528)",
        industry_standards=["Police Check", "Security check"],
        competency=["top rated", "experienced"],
        location="Sydney",
        start_date=date,
        availability=True,
        hours_per_week=10,
        duration="2 months",
        fees_from=200,
    )

    assert request.course_name == "Bachelor of Community Services (HE20528)"
    assert request.industry_standards == ["Police Check", "Security check"]
    assert request.competency == ["top rated", "experienced"]
    assert request.location == "Sydney"
    assert request.start_date == date
    assert request.availability is True
    assert request.hours_per_week == 10
    assert request.duration == "2 months"
    assert request.fees_from == 200
