from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    id: str
    email: str
    created_at: str
    updated_at: str
    user_metadata: dict = {}
    app_metadata: dict = {}

class CreateUserRequest(BaseModel):
    email: str
    password: str
    user_metadata: Optional[dict] = {}

class UpdateProfileRequest(BaseModel):
    user_metadata: dict
