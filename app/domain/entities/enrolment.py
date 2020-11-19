from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Enrolment(BaseModel):
    enrolment_id: str
    shared_secret: str
    internal_reference: str
    created: datetime = Field(default_factory=datetime.now)


class EnrolmentFilters(BaseModel):
    course_id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    receive_date: Optional[datetime]
