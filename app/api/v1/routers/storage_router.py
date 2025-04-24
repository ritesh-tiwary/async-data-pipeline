from io import BytesIO
from typing import Annotated
from functools import lru_cache
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Depends, Header, Request, status
from app.api.v1.services.storage_service import StorageService


router = APIRouter(
    prefix="/storage",
    tags=["storage"],
    responses={404: {"description": "Not found"}}
)

@lru_cache()
def get_storage_service() -> StorageService:
    """
    Initialize the StorageService with a directory for storing files.
    """
    return StorageService()

@router.get("/")
async def read_storage_items():
    """
    Endpoint to retrieve all storage items.
    """
    return {"message": "List of storage items"}

@router.post("/upload")
async def upload_file(request: Request,
                      x_mapping: Annotated[str, Header()],
                      x_checksum: Annotated[str, Header()],
                      x_filename: Annotated[str, Header()],
                      storage_service: Annotated[StorageService, Depends(get_storage_service)]):
    """
    Endpoint to upload a new file.
    """
    total_chunks = 0
    fileobj = BytesIO()
    async for chunk in request.stream():
        if total_chunks < 1e8:  # ~100MB limit
            total_chunks += len(chunk)
            if total_chunks > 0:
                fileobj.write(chunk)
            else:
                return JSONResponse(
                    content={"detail": f"Empty file - {x_filename}"},
                    status_code=status.HTTP_411_LENGTH_REQUIRED
                )

    if storage_service.validate_checksum(x_checksum, fileobj):
        task_id = storage_service.upload_file(x_mapping, x_filename, fileobj)
    else:
        return JSONResponse(
            content={"detail": f"Incorrect checksum - {x_checksum}"},
            status_code=status.HTTP_412_PRECONDITION_FAILED
        )
    return {"FileName": x_filename, "Message": f"Upload complete. The file is now in the processing queue.Task Id: {task_id}"}

@router.delete("/{item_id}")
async def delete_storage_item(item_id: int):
    """
    Endpoint to delete a storage item by ID.
    """
    return {"message": f"Storage item with ID {item_id} deleted"}