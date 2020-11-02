from pydantic import BaseModel

from app.repositories.user_repo import UserRepo
from app.requests.user_requests import CreateUserRequest
from app.responses import ResponseFailure, ResponseSuccess
from app.utils import Random


class CreateNewUser(BaseModel):
    user_repo: UserRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, create_user_request: CreateUserRequest):
        create_user_dict = create_user_request.dict()
        create_user_dict["user_id"] = str(Random.get_uuid())

        try:
            course = self.user_repo.create_user(user_dict=create_user_dict)
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=course)
