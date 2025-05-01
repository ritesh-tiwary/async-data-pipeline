from uuid import UUID
from typing import Annotated
from fastapi import Header, HTTPException, status


async def get_request_id_header(X_Request_Id: Annotated[str, Header()]):
    try:
        UUID(X_Request_Id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Header - X-Request-Id')