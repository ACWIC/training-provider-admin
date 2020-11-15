from pydantic import BaseModel

from app.repositories.industry_standard_repo import IndustryStandardRepo
from app.requests.industry_standard_request import IndustryStandardRequest
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class PostIndustryStandard(BaseModel):
    industry_standard_repo: IndustryStandardRepo

    class Config:
        # Pydantic will complain if something (industry_standard_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, industry_standard_request: IndustryStandardRequest):
        try:
            industry_standard = self.industry_standard_repo.post_industry_standard(
                industry_standard_request
            )
            code = SuccessType.CREATED
            message = "The industry_standard has been created."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=industry_standard, message=message, type=code)
