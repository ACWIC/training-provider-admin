import abc
from typing import List

from app.domain.entities.enrolment_request import EnrolmentAuth, EnrolmentAuthFilters


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def get_enrolments(
        self, enrolment_filters: EnrolmentAuthFilters
    ) -> List[EnrolmentAuth]:
        """"""

    @abc.abstractmethod
    def get_enrolment_auth_by_id(self, enrolment_request_id: str) -> EnrolmentAuth:
        """"""

    @abc.abstractmethod
    def update_enrolment_state(
        self, enrolment: EnrolmentAuth, new_state: str
    ) -> EnrolmentAuth:
        """"""

    @abc.abstractmethod
    def enrolment_auth_exists(self, enrolment_request_id: str) -> bool:
        """"""
