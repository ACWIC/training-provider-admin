from datetime import datetime

from app.requests import ValidRequest


class NewIndustryStandard(ValidRequest):
    # standard_id: str
    standard_title: str
    standard_version: str
    standard_status: str
    status_attained_date: datetime
    review_date: datetime
    competencies_list: list
