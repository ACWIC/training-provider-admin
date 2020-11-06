from typing import Optional

from pydantic import BaseModel, Field

from app.utils import Random


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    user_id: str = Field(default_factory=Random().get_uuid)
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

    def serialize(self):
        return bytes(self.json(), "utf-8")
