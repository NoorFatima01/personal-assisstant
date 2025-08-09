from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum

class ChatStatus(str, Enum):
    active = "active"
    complete = "complete"

class ChatResponse(BaseModel):
    messages: List[dict] = Field(..., description="List of messages in the chat response.")
    user_id: str = Field(..., description="Unique identifier for the user.")
    id: str = Field(..., description="Unique identifier for the chat response.")
    created_at: str = Field(..., description="Timestamp when the chat response was created.")
    status: ChatStatus = Field(..., description="Status of the chat response.")
    messages_count: int = Field(..., description="Number of messages in the chat response.")
    updated_at: str = Field(..., description="Timestamp when the chat response was last updated.")

class ChatResponseModel(BaseModel):
    data: Optional[ChatResponse] = Field(None, description="Chat session data")
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Response status (success/error)")