from typing import Optional

from app.requests import ValidRequest


class CreateUserRequest(ValidRequest):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
