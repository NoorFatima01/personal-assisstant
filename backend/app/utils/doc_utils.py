from fastapi import HTTPException
import json


def validate_pdf_files(files: dict):
    print("Validating PDF files...")
    for file_type, file in files.items():
        if file.content_type != 'application/pdf' or not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"{file_type} file must be a valid PDF"
            )

def format_sse(event_type: str, data: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
