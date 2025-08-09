from typing import Dict
from fastapi import UploadFile
from ...utils.doc_utils import validate_pdf_files, process_documents_task
from ..user_services.user_db_service import UserDBService
from .file_mngmnt_service import LocalFileManager

class DocumentUploadService:    
    def __init__(self):
        self.user_db_service = UserDBService()
        self.file_manager = LocalFileManager()

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

        temp_paths = await self.file_manager.save_temporary_files(list(files_dict.values()), user_id, list(files_dict.keys()))

        process_documents_task.delay(temp_paths, user_id, week_start)

        return {"message": "Document processing started in the background"}
