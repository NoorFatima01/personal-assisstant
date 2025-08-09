import os
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, Form
from fastapi.responses import JSONResponse
from app.dependencies.auth import verify_token
from app.services.doc_services.doc_upload_service import DocumentUploadService
from app.schemas.doc_schema import DocUploadRequest, DocUploadResponse


router = APIRouter()
document_upload_service = DocumentUploadService()

@router.post("/upload_doc", response_model=DocUploadResponse)
async def upload_docs(
    work: UploadFile = File(...),
    health: UploadFile = File(...),
    reflections: UploadFile = File(...),
    personal: UploadFile = File(...),
    week_start: str = Form(...),
    userId: str = Depends(verify_token)
):
    try:
        # Validate the form data using your Pydantic model
        request_data = DocUploadRequest(week_start=week_start)
        result = await document_upload_service.handle_document_upload(work, health, reflections, personal, request_data.week_start, userId)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

