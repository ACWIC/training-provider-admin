import json
from typing import Any

import boto3

from app.config import settings
from app.domain.entities.industry_standard import IndustryStandard
from app.repositories.industry_standard_repo import IndustryStandardRepo
from app.requests.industry_standard_request import NewIndustryStandard
from app.utils import Random
from app.utils.error_handling import handle_s3_errors


class S3IndustryStandardRepo(IndustryStandardRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with handle_s3_errors():
            self.s3 = boto3.client("s3", **settings.s3_configuration)

    def post_industry_standard(
        self, industry_standard_request: NewIndustryStandard
    ) -> IndustryStandard:
        input_standard = industry_standard_request.dict()
        input_standard["standard_id"] = Random.get_uuid()
        industry_standard = IndustryStandard(**input_standard)
        with handle_s3_errors():
            self.s3.put_object(
                Body=bytes(industry_standard.json(), "utf-8"),
                Key=f"industry_standards/{industry_standard.standard_id}.json",
                Bucket=settings.STANDARDS_BUCKET,
            )
        return industry_standard

    def delete_industry_standard(self, standard_id: str):
        with handle_s3_errors():
            response = self.s3.delete_object(
                Bucket=settings.STANDARDS_BUCKET,
                Key=f"industry_standards/{standard_id}.json",
            )
        return response

    def get_standards(self) -> dict:
        with handle_s3_errors():
            standards_objects_list = self.s3.list_objects(
                Bucket=settings.STANDARDS_BUCKET,
                Prefix="{}/".format("industry_standards"),
            )
        print("Contents", standards_objects_list.get("Contents", []))
        standards_list = []
        for standards_object in standards_objects_list.get("Contents", []):
            with handle_s3_errors():
                standards_object = self.s3.get_object(
                    Key=standards_object["Key"], Bucket=settings.STANDARDS_BUCKET
                )
            standard = IndustryStandard(
                **json.loads(standards_object["Body"].read().decode())
            )
            standards_list.append({"standard": standard.dict()})
        return {"standards_list": standards_list}

    def standard_exists(self, standard_id: str) -> bool:
        try:
            self.s3.get_object(
                Key=f"industry_standards/{standard_id}.json",
                Bucket=settings.STANDARDS_BUCKET,
            )
            return True
        except Exception:
            return False
