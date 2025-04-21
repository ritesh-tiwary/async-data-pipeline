import os
import shutil
import hashlib
from io import BytesIO
from typing import List
from fastapi import HTTPException, UploadFile
from app.worker.tasks import save_data


class StorageService:
    def __init__(self):...        

    def validate_checksum(self, checksum: str, content: bytes) -> bool:
        md5_hash = hashlib.md5()
        md5_hash.update(content)

        calculated_checksum = md5_hash.hexdigest()
        return calculated_checksum == checksum
    
    def upload_file(self, filename: str, content: bytes) -> str:
        task = save_data.delay(filename, content)
        return task.id

    def delete_file(self, file_name: str, sub_dir: str = "") -> None:
        try:
            file_path = os.path.join(self.storage_dir, sub_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                raise HTTPException(status_code=404, detail="File not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    def list_files(self, sub_dir: str = "") -> List[str]:
        try:
            target_dir = os.path.join(self.storage_dir, sub_dir)
            if not os.path.exists(target_dir):
                raise HTTPException(status_code=404, detail="Directory not found")

            return os.listdir(target_dir)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")