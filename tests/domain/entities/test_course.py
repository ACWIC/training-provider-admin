import datetime
from uuid import uuid4

from app.domain.entities.course import Course


def test_course_init():
    """
    Ensure the course data matches constructor values
    """
    course_id = str(uuid4())
    created = datetime.datetime.now()
    date = datetime.datetime.now()

    course = Course(
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
        created=created,
    )

    assert course.course_id == course_id
    assert course.course_name == "Bachelor of Community Services (HE20528)"
    assert course.industry_standards == "Police Check"
    assert course.competency == "top rated"
    assert course.location == "Sydney"
    assert course.date == date
    assert course.availability is True
    assert course.hours_per_week == 10
    assert course.duration == "2 months"
    assert course.fees_from == 200
    assert course.created == created
