from datetime import datetime

from app.requests import ValidRequest


class NewCourseRequest(ValidRequest):
    # course_id: str
    course_name: str
    industry_standards: list
    competency: list
    location: str
    start_date: datetime
    availability: bool
    hours_per_week: float
    duration: str
    fees_from: float
    # created: datetime
