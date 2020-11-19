from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Enrolment(BaseModel):
    enrolment_id: str
    shared_secret: str
    internal_reference: str
    created: datetime = Field(default_factory=datetime.now)


class EnrolmentFilters(BaseModel):
    course_id: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    receive_date: Optional[str]
