from .vector_store_embed_service import QdrantVectorStoreEmbedService
from .storage_db_service import SupabaseStorageDBService
from .file_mngmnt_service import LocalFileManager
from fastapi import HTTPException
from typing import List
from ..user_services.user_db_service import UserDBService


class ProcessDocumentService:
    """Main service orchestrating document operations"""
    
    def __init__(self):
        self.storage_db_service = SupabaseStorageDBService()
        self.vector_store_embed_service = QdrantVectorStoreEmbedService()
        self.file_manager = LocalFileManager()
        self.user_db_service = UserDBService()

    def process_documents_sync(self, temp_paths: List[str], user_id: str, week_start: str) -> dict:
        """Process documents synchronously"""
        try:
            # Upload files to storage
            public_urls = self.storage_db_service.upload_files(temp_paths, user_id, week_start)

            # Save metadata to database
            self.storage_db_service.save_document_metadata(temp_paths, user_id, week_start, public_urls)

            # Embed documents
            self.vector_store_embed_service.embed_documents(temp_paths, user_id, week_start)

            # Update user weeks in the database
            self.user_db_service.update_user_weeks(user_id, week_start)
        except Exception as e:
            print(f"Error processing documents: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if temp_paths:
                # Cleanup temporary files
                self.file_manager.cleanup_files(temp_paths)

    # async def process_documents(self, files: List[UploadFile], user_id: str, file_types: List[str], week_start: str) -> dict:
    #     """Process documents through the entire pipeline"""
    #     temp_paths = []
    #     try:
    #         # Save files temporarily
    #         temp_paths = await self.file_manager.save_temporary_files(files, user_id, file_types)
            
    #         # Upload to storage
    #         public_urls = self.storage_db_service.upload_files(temp_paths, user_id, week_start)
            
    #         # Save metadata to database
    #         self.storage_db_service.save_document_metadata(temp_paths, user_id, week_start, public_urls)
    #         # Embed documents
    #         self.vector_store_embed_service.embed_documents(temp_paths, user_id, week_start)
    #         return {
    #             "message": "Documents uploaded and processed successfully",
    #             "public_urls": public_urls
    #         }
            
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))
            
    #     finally:
    #         # Always cleanup temporary files
    #         if temp_paths:
    #             self.file_manager.cleanup_files(temp_paths)