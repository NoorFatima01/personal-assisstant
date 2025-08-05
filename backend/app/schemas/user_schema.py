from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    id: str
    email: str
    firstname: str
    lastname: str
    created_at: str
    weeks: Optional[list[str]] = None

