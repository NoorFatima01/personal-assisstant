from pydantic import BaseModel, Field, field_validator


class DocUploadRequest(BaseModel):
    week_start: str = Field(..., description="week_start of the year")

    @field_validator("week_start")
    def validate_week_start(cls, v):
        if not v:
            raise ValueError("week_start must be provided")
        if not isinstance(v, str):
            raise ValueError("week_start must be a string")
        return v


class DocUploadResponse(BaseModel):
    message: str
    # uploaded_files: list[str]
    # week_start: Date
