import abc
from typing import List

from app.domain.entities.enrolment import Enrolment, EnrolmentFilters


class EnrolmentRepo(abc.ABC):
    @abc.abstractmethod
    def get_enrolments(self, enrolment_filters: EnrolmentFilters) -> List[Enrolment]:
        """"""
