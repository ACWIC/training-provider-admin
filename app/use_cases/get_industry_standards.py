from pydantic import BaseModel

from app.repositories.industry_standard_repo import IndustryStandardRepo
from app.responses import ResponseFailure, ResponseSuccess


class GetIndustryStandards(BaseModel):
    industry_standard_repo: IndustryStandardRepo

    class Config:
        # Pydantic will complain if something (industry_standard_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self):
        try:
            response = self.industry_standard_repo.get_standards()
            message = "The industry_standard has been fetched."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=response, message=message)
