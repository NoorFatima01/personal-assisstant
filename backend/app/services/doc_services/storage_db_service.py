from mimetypes import guess_type
import os
from typing import Tuple, List
from app.config.supabase_client import supabase
from fastapi import HTTPException


class SupabaseStorageDBService:
    def __init__(self, bucket_name:str = "goals-pdfs", table_name:str = "uploaded_docs"):
        self.bucket_name = bucket_name
        self.table_name = table_name
        self.supabase = supabase

    def upload_files(self, temp_paths: List[Tuple[str, str]], user_id: str, week_start: str) -> List[str]:
        public_urls = []
        try:
            for file_path, file_type in temp_paths:
                filename = os.path.basename(file_path)
                storage_path = f"{user_id}/{file_type}/{week_start}_{filename}"
                with open(file_path, "rb") as f:
                    mime_type = guess_type(file_path)[0] or "application/pdf"
                    file_bytes = f.read()
                    try:
                        response = self.supabase.storage.from_(self.bucket_name).upload(
                            storage_path,
                            file_bytes,
                            file_options={"content-type": mime_type}
                        )
                    except Exception as upload_error:
                        raise Exception(f"Supabase upload error: {str(upload_error)}")

                public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(storage_path)
                public_urls.append(public_url)


            return public_urls

        except Exception as e:
            raise e
        
    def save_document_metadata(self, temp_paths: List[Tuple[str, str]], user_id: str, week_start: str, public_urls: List[str]) -> None:
        
        try:
            for (file_path, file_type), public_url in zip(temp_paths, public_urls):
                file_name = os.path.basename(file_path)
                self.supabase.table(self.table_name).insert({
                    "user_id": user_id,
                    "file_name": file_name,
                    "week_start": week_start,
                    "public_url": public_url,
                    "file_type": file_type
                }).execute()
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database insert error: {str(e)}")

    