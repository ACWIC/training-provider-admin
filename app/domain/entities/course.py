from datetime import datetime

from pydantic import BaseModel


class Course(BaseModel):
    course_id: str
    course_name: str
    industry_standards: list
    competency: list
    location: str
    start_date: datetime
    availability: bool
    hours_per_week: float
    duration: str
    fees_from: float
    created: datetime
