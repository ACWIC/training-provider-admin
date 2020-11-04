from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.config import settings
from app.domain.entities.user import Token
from app.repositories.user_repo import UserRepo
from app.responses import ResponseFailure, ResponseSuccess, SuccessType


class CreateAccessToken(BaseModel):
    user_repo: UserRepo

    class Config:
        # Pydantic will complain if something (course_repo) is defined
        # as having a non-BaseModel type (e.g. an ABC). Setting this ensures
        # that it will just check that the value isinstance of this class.
        arbitrary_types_allowed = True

    def execute(self, form_data: OAuth2PasswordRequestForm):
        user = self.user_repo.authenticate_user(form_data.username, form_data.password)
        if not user:
            return ResponseFailure.build_from_unauthorised_error(
                message="Incorrect username or password"
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        try:
            access_token = self.user_repo.create_access_token(
                subject={"sub": user.username}, expires_delta=access_token_expires
            )
            token = Token(access_token=access_token, token_type="bearer")
            code = SuccessType.CREATED
            message = "Token is created."
        except Exception as e:
            return ResponseFailure.build_from_resource_error(message=e)

        return ResponseSuccess(value=token, type=code, message=message)
