import abc
from typing import List

from app.domain.entities.enrolment_request import EnrolmentFilters, EnrolmentRequest


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def get_enrolments(
        self, enrolment_filters: EnrolmentFilters
    ) -> List[EnrolmentRequest]:
        """"""

    @abc.abstractmethod
    def get_enrolment_by_id(self, enrolment_request_id: str) -> EnrolmentRequest:
        """"""

    @abc.abstractmethod
    def update_enrolment_state(
        self, enrolment: EnrolmentRequest, new_state: str
    ) -> EnrolmentRequest:
        """"""
