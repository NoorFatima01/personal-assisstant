import os
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, Form
from fastapi.responses import JSONResponse
from app.dependencies.auth import verify_token
from app.controllers.doc_controller import DocumentController


router = APIRouter()
document_controller = DocumentController()


@router.post("/upload_doc")
async def upload_docs(
    work: UploadFile = File(...),
    health: UploadFile = File(...),
    reflections: UploadFile = File(...),
    personal: UploadFile = File(...),
    week_start: str = Form(...),
    userId: str = Depends(verify_token)
):
    try:
        result = await document_controller.handle_document_upload(work, health, reflections, personal, week_start, userId)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

