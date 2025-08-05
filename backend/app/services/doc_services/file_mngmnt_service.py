import os
import tempfile
from typing import Tuple, List
from fastapi import HTTPException, UploadFile

class LocalFileManager:
    """Handles temporary file operations"""
    
    async def save_temporary_files(self, files: List[UploadFile], user_id: str, file_types: List[str]) -> List[Tuple[str, str]]:
        """Save uploaded files temporarily and return file paths with types"""
        file_paths = []
        
        for file, file_type in zip(files, file_types):
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, f"{file_type}_{user_id}_{file.filename}")
            
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
                
            file_paths.append((file_path, file_type))
            
        return file_paths
    
    def cleanup_files(self, file_paths: List[Tuple[str, str]]) -> None:
        """Clean up temporary files"""
        for file_path, _ in file_paths:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error removing file {file_path}: {e}")
                    raise HTTPException(status_code=500, detail=f"Error removing file {file_path}: {e}")
