from datetime import datetime

from pydantic import BaseModel


class IndustryStandard(BaseModel):
    standard_id: str
    standard_title: str
    standard_version: str
    standard_status: str
    status_attained_date: datetime
    review_date: datetime
    competencies_list: list


class IndustryStandardV2(BaseModel):
    standard_id: str
    standard_title: str
    standard_version: str
    standard_status: str
    status_attained_date: datetime
    review_date: datetime
    competencies_list: list
    description: str
