from datetime import datetime
from typing import Optional

from app.requests import ValidRequest


class UpdateCourseRequest(ValidRequest):
    course_id: str
    course_name: Optional[str]
    industry_standards: Optional[list]
    competency: Optional[list]
    location: Optional[str]
    start_date: Optional[datetime]
    availability: Optional[bool]
    hours_per_week: Optional[float]
    duration: Optional[str]
    fees_from: Optional[float]
    # created: datetime
