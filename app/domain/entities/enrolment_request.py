from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class State(str, Enum):
    NEW = "new"
    INFO_REQUESTED = "info_requested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    WITHDRAWN = "withdrawn"
    COMPLETED = "completed"


VALID_STATE_CHANGES = (
    (State.NEW, State.ACCEPTED),
    (State.NEW, State.REJECTED),
    (State.NEW, State.INFO_REQUESTED),
    (State.INFO_REQUESTED, State.ACCEPTED),
    (State.INFO_REQUESTED, State.REJECTED),
    (State.INFO_REQUESTED, State.INFO_REQUESTED),
    (State.ACCEPTED, State.CANCELLED),
    (State.ACCEPTED, State.WITHDRAWN),
    (State.ACCEPTED, State.COMPLETED),
)


class EnrolmentStatus(str, Enum):
    lodged = "Lodged"


class EnrolmentAuth(BaseModel):
    enrolment_auth_id: str
    student_id: str
    course_id: str
    status: EnrolmentStatus = EnrolmentStatus.lodged
    enrolment_id: str
    shared_secret: str
    created: datetime = Field(default_factory=datetime.now)
    state: State


class EnrolmentAuthFilters(BaseModel):
    course_id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    receive_date: Optional[datetime]
    state: Optional[List]