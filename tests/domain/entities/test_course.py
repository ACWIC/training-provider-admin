import datetime
from uuid import uuid4

from app.domain.entities.course import Course


def test_course_init():
    """
    Ensure the enrollment data matches constructor values
    and the status is appropriately set.
    """
    course_id = str(uuid4())
    created = str(datetime.datetime.now())

    course = Course(
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
        created=created,
    )

    assert course_id == course.course_id
    assert "Bachelor of Community Services (HE20528)" == course.course_name
    assert "Police Check" == course.industry_standards
    assert "top rated" == course.competancy
    assert "Sydney" == course.location
    assert "2020-10-11T16:06:53.739338" == course.date
    assert "morning" == course.availablity
    assert "10" == course.hours_per_week
    assert "2 months" == course.duration
    assert "200" == course.fees_from
    assert created == course.created
