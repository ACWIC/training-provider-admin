from datetime import datetime
from typing import Optional

from app.requests import ValidRequest


class UpdateCourseRequest(ValidRequest):
    course_id: str
    course_name: Optional[str]
    industry_standards: Optional[str]
    competency: Optional[str]
    location: Optional[str]
    date: Optional[datetime]
    availability: Optional[bool]
    hours_per_week: Optional[float]
    duration: Optional[str]
    fees_from: Optional[float]
    # created: datetime
