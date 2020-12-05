import json
from typing import Any, List

import boto3

from app.config import settings
from app.domain.entities.enrolment_request import (
    VALID_STATE_CHANGES,
    EnrolmentAuth,
    EnrolmentAuthFilters,
)
from app.repositories.enrolment_repo import EnrolmentRepo
from app.utils.error_handling import handle_s3_errors


class S3EnrolmentRepo(EnrolmentRepo):
    s3: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with handle_s3_errors():
            self.s3 = boto3.client("s3", **settings.s3_configuration)

    def get_enrolments(
        self, enrolment_filters: EnrolmentAuthFilters
    ) -> List[EnrolmentAuth]:
        enrolment_filters = enrolment_filters.dict()
        with handle_s3_errors():
            enrolment_objects_list = self.s3.list_objects(
                Bucket=settings.ENROLMENT_AUTHORISATION_BUCKET
            )
        enrolments_list = []
        for enrolments_object in enrolment_objects_list.get("Contents", []):
            with handle_s3_errors():
                obj = self.s3.get_object(
                    Key=f"enrolment_authorisations/{enrolments_object['Key']}.json",
                    Bucket=settings.ENROLMENT_AUTHORISATION_BUCKET,
                )
            enrolment = json.loads(obj["Body"].read().decode())
            enrolment = EnrolmentAuth(**enrolment).dict()
            if filters_match(enrolment, enrolment_filters.copy()):
                enrolments_list.append(enrolment)

        return enrolments_list

    def get_enrolment_auth_by_id(self, enrolment_request_id: str) -> EnrolmentAuth:
        with handle_s3_errors():
            obj = self.s3.get_object(
                Key=f"enrolment_authorisations/{enrolment_request_id}.json",
                Bucket=settings.ENROLMENT_AUTHORISATION_BUCKET,
            )
        enrolment = EnrolmentAuth(**json.loads(obj["Body"].read().decode()))
        return enrolment

    def enrolment_auth_exists(self, enrolment_request_id: str) -> bool:
        try:
            self.s3.get_object(
                Key=f"enrolment_authorisations/{enrolment_request_id}.json",
                Bucket=settings.ENROLMENT_AUTHORISATION_BUCKET,
            )
            return True
        except Exception:
            return False

    def update_enrolment_state(
        self, enrolment: EnrolmentAuth, new_state: str
    ) -> EnrolmentAuth:
        new_enrolment = enrolment.dict()
        new_enrolment.update({"state": new_state})
        new_enrolment = EnrolmentAuth(**new_enrolment)
        with handle_s3_errors():
            self.s3.put_object(
                Body=bytes(new_enrolment.json(), "utf-8"),
                Key=f"enrolment_authorisations/{new_enrolment.enrolment_id}.json",
                Bucket=settings.ENROLMENT_AUTHORISATION_BUCKET,
            )
        return new_enrolment


def filters_match(enrolment: dict, enrolment_filters: dict):
    # if enrolment created_date is in a specific range
    date_in_range = if_dates_in_range(enrolment, enrolment_filters)
    # Keep only those keys that are mutual in both
    # enrolment and enrolment_filters and are not None
    compare_enrolment = {
        k: v for (k, v) in enrolment.items() if enrolment_filters.get(k) is not None
    }
    enrolment_filters = dict(
        (k, v) for k, v in enrolment_filters.items() if k in enrolment and v is not None
    )
    # final check
    if compare_enrolment == enrolment_filters and date_in_range:
        return True
    return False


def if_dates_in_range(enrolment: dict, enrolment_filters: dict):
    date_in_range = True
    if enrolment_filters.get("start_date") and enrolment_filters.get("end_date"):
        date_in_range = False
        if (
            enrolment_filters["start_date"].replace(tzinfo=None)
            <= enrolment["created"]
            <= enrolment_filters["end_date"].replace(tzinfo=None)
        ):
            date_in_range = True
    elif enrolment_filters.get("receive_date"):
        date_in_range = (
            enrolment["created"].date() == enrolment_filters["receive_date"].date()
        )

    return date_in_range


def state_change_valid(current_state, new_state) -> bool:
    if (current_state, new_state) in VALID_STATE_CHANGES:
        return True
    return False
