from datetime import datetime

from pydantic import BaseModel


class Course(BaseModel):
    course_id: str
    course_name: str
    industry_standards: str
    competency: str
    location: str
    date: datetime
    availability: bool
    hours_per_week: float
    duration: str
    fees_from: float
    created: datetime
