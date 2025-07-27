from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional

class AskResponse(BaseModel):
    answer: str
    source: str

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=8, max_length=350, description="The question to ask the assistant.")

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
    
class QuestionResponse(BaseModel):
    answer: str = Field(..., description="The answer provided by the assistant.")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional metadata about the question and answer, such as source or context."
    )
    processing_time_ms: float = Field(..., description="Time taken to process the question and generate the answer in milliseconds.")
    source_used: Optional[str] = Field(
        default=None, description="The source document or context used to generate the answer, if applicable."
    )

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message describing what went wrong.")
    error_type: Optional[str] = Field(
        default=None, description="Type of error that occurred, if applicable (e.g., 'ValidationError', 'InternalServerError').")
    request_id: Optional[str] = Field(
        default=None, description="Unique identifier for the request, useful for debugging and tracing errors.")

# Internal models for service layer communication
# class ClassificationResult(BaseModel):
#     """Internal model for classification results"""
#     category: str
#     confidence: Optional[float] = None
#     attempts: int = 1

class RetrievalResult(BaseModel):
    """Internal model for document retrieval results"""
    classification: str
    context: str
    sources_count: int
    question: str  

class ProcessingResult(BaseModel):
    """Internal model for complete processing results"""
    answer: str
    classification: str
    context_sources: int
    metadata: Dict[str, Any] = Field(default_factory=dict)