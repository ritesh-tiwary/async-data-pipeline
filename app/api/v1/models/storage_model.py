from pydantic import BaseModel


class FileTaskPayload(BaseModel):
    filename: str
    filepath: str
    info: dict = {}  # Optional metadata
