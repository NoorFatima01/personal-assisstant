from typing import Dict
from fastapi import UploadFile
from ..utils.doc_utils import validate_pdf_files
from ..services.user_services.user_db_service import UserDBService
from ..services.doc_services.process_doc_service import ProcessDocumentService

class DocumentController:    
    def __init__(self):
        self.document_service = ProcessDocumentService()
        self.user_db_service = UserDBService()

    async def handle_document_upload(
        self,
        work: UploadFile,
        health: UploadFile,
        reflections: UploadFile,
        personal: UploadFile,
        week_start: str,
        user_id: str
    ) -> Dict:
        """Handle document upload logic"""
        files_dict = {"work": work, "health": health, "reflections": reflections, "personal": personal}

        validate_pdf_files(files_dict)
        self.user_db_service.update_user_weeks(user_id, week_start)
        
        return await self.document_service.process_documents(
            files=list(files_dict.values()),
            user_id=user_id,
            file_types=list(files_dict.keys()),
            week_start=week_start
        )