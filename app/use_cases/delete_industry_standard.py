from pydantic import BaseModel

from app.repositories.industry_standard_repo import IndustryStandardRepo
from app.responses import ResponseFailure, ResponseSuccess


class DeleteIndustryStandard(BaseModel):
    industry_standard_repo: IndustryStandardRepo

    class Config:
        # Pydantic will complain if something (industry_standard_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, standard_id: str):
        try:
            # Check if course with course_id exists
            if not self.industry_standard_repo.standard_exists(standard_id):
                return ResponseFailure.build_from_validation_error(
                    message=f"Standard_id={standard_id} is invalid."
                )
            industry_standard = self.industry_standard_repo.delete_industry_standard(
                standard_id
            )
            message = "The industry_standard has been deleted."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=industry_standard, message=message)
