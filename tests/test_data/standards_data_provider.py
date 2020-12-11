import datetime

from app.domain.entities.industry_standard import IndustryStandard
from app.requests.industry_standard_request import IndustryStandardRequest


class StandardsDataProvider:
    standard_id: str
    standard_title: str
    standard_version: str
    standard_status: str
    status_attained_date: datetime
    review_date: datetime
    competencies_list: list

    def __init__(self):
        date_time_str = "2018-06-29 08:15:27.243860"
        date = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
        self.created = date

        self.standard_id = "1dad3dd8-af28-4e61-ae23-4c93a456d10e"
        self.standard_title = "standard_title"
        self.standard_version = "standard_version"
        self.standard_status = "standard_status"
        self.status_attained_date = date
        self.review_date = date
        self.competencies_list = []

        self.industry_standard = IndustryStandard(
            standard_id=self.standard_id,
            standard_title=self.standard_title,
            standard_version=self.standard_version,
            standard_status=self.standard_status,
            status_attained_date=self.status_attained_date,
            review_date=self.review_date,
            competencies_list=self.competencies_list,
        )

        self.industry_standard_request = IndustryStandardRequest(
            standard_title=self.standard_title,
            standard_version=self.standard_version,
            standard_status=self.standard_status,
            status_attained_date=self.status_attained_date,
            review_date=self.review_date,
            competencies_list=self.competencies_list,
        )

        self.industry_standard_list = {
            "standards_list": [{"standard": self.industry_standard.json()}]
        }

        self.delete_standard_response = {
            "ResponseMetadata": {
                "RequestId": "164DD512D5F24240",
                "HostId": "",
                "HTTPStatusCode": 204,
                "HTTPHeaders": {
                    "accept-ranges": "bytes",
                    "content-security-policy": "block-all-mixed-content",
                    "server": "MinIO/RELEASE.2020-10-28T08-16-50Z",
                    "vary": "Origin",
                    "x-amz-request-id": "164DD512D5F24240",
                    "x-xss-protection": "1; mode=block",
                    "date": "Sat, 05 Dec 2020 13:28:38 GMT",
                },
                "RetryAttempts": 0,
            }
        }
