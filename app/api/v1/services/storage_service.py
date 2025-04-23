import os
import shutil
import hashlib
from celery import chain
from typing import List, BinaryIO
from fastapi import HTTPException, UploadFile
from app.core.base import Base
from app.worker.tasks import parse_data, load_data
from app.api.v1.models.storage_model import FileTaskPayload


class StorageService(Base):
    def __init__(self):
        super().__init__()
        self.storage_dir = self.settings.STORAGE_DIR

    def validate_checksum(self, checksum: str, fileobj: BinaryIO) -> bool:
        md5_hash = hashlib.md5()
        md5_hash.update(fileobj.getvalue())

        calculated_checksum = md5_hash.hexdigest()
        return calculated_checksum == checksum
    
    def upload_file(self, file_name: str, fileobj: BinaryIO) -> str:
        file_path = os.path.join(self.storage_dir, file_name)
        with open(file_path, 'wb') as f:
            fileobj.seek(0)
            shutil.copyfileobj(fileobj, f)

        payload = FileTaskPayload(filename=file_name, filepath=file_path, info={"mapping": "mapping/mapping_tablename_jsonfilename.csv", "source": "api"})
        chain_task = chain(parse_data.s(payload.dict()), load_data.s(payload.dict())).delay()
        return chain_task.id

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