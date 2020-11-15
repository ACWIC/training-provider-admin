import abc

from app.domain.entities.industry_standard import IndustryStandard
from app.requests.industry_standard_request import IndustryStandardRequest


class IndustryStandardRepo(abc.ABC):
    @abc.abstractmethod
    def post_industry_standard(
        self, industry_standard_request: IndustryStandardRequest
    ) -> IndustryStandard:
        pass

    @abc.abstractmethod
    def delete_industry_standard(self, standard_id: str):
        pass

    @abc.abstractmethod
    def get_standards(self) -> dict:
        pass

    @abc.abstractmethod
    def standard_exists(self, standard_id: str) -> bool:
        pass
