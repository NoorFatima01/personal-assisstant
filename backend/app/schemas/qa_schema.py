from pydantic import BaseModel, Field, field_validator
from typing import List

# class AskResponse(BaseModel):
#     answer: str
#     source: str

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=8, max_length=150, description="The question to ask the assistant.")
    chat_id: str = Field(..., description="Unique identifier for the chat session.")
    week_start: List[str] = Field(
        default=None, description="Week start date for context, if applicable."
    )

    @field_validator('question')
    def validate_question(cls, value):
        if not value.strip():
            raise ValueError("Question cannot be empty or whitespace.")

        cleaned_value = value.strip()

        if len(cleaned_value) < 8:
            raise ValueError("Question must be at least 8 characters long.")
        if len(cleaned_value) > 350:
            raise ValueError("Question must not exceed 350 characters.")

        return cleaned_value
    
# class QuestionResponse(BaseModel):
#     answer: str = Field(..., description="The answer provided by the assistant.")
#     metadata: Optional[Dict[str, Any]] = Field(
#         default=None, description="Optional metadata about the question and answer, such as source or context."
#     )
#     processing_time_ms: float = Field(..., description="Time taken to process the question and generate the answer in milliseconds.")
#     source_used: Optional[str] = Field(
#         default=None, description="The source document or context used to generate the answer, if applicable."
#     )