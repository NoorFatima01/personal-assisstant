from fastapi import HTTPException
from app.config.celery_app import celery_app
from app.services.doc_services.process_doc_service import ProcessDocumentService

def validate_pdf_files(files: dict):
    for file_type, file in files.items():
        if file.content_type != 'application/pdf' or not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"{file_type} file must be a valid PDF"
            )

@celery_app.task
def process_documents_task(temp_paths, user_id, week_start):
    """Runs in the background to process documents"""
    service = ProcessDocumentService()
    service.process_documents_sync(temp_paths, user_id, week_start)
    return {"status": "completed"}