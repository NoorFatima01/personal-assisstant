from .vector_store_embed_service import QdrantVectorStoreEmbedService
from .storage_db_service import SupabaseStorageDBService
from .file_mngmnt_service import LocalFileManager
from fastapi import UploadFile, HTTPException
from typing import List


class ProcessDocumentService:
    """Main service orchestrating document operations"""
    
    def __init__(self):
        self.storage_db_service = SupabaseStorageDBService()
        self.vector_store_embed_service = QdrantVectorStoreEmbedService()
        self.file_manager = LocalFileManager()
    
    async def process_documents(self, files: List[UploadFile], user_id: str, file_types: List[str], week_start: str) -> dict:
        """Process documents through the entire pipeline"""
        temp_paths = []
        print(f"Processing documents for user {user_id} with week start {week_start}")
        try:
            # Save files temporarily
            temp_paths = await self.file_manager.save_temporary_files(files, user_id, file_types)
            
            # Upload to storage
            public_urls = self.storage_db_service.upload_files(temp_paths, user_id, week_start)
            
            # Save metadata to database
            self.storage_db_service.save_document_metadata(temp_paths, user_id, week_start, public_urls)
            # Embed documents
            self.vector_store_embed_service.embed_documents(temp_paths, user_id, week_start)
            return {
                "message": "Documents uploaded and processed successfully",
                "public_urls": public_urls
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            
        finally:
            # Always cleanup temporary files
            if temp_paths:
                self.file_manager.cleanup_files(temp_paths)