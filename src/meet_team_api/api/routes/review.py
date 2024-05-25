from typing import Annotated

from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

review_router = APIRouter()


@review_router.get(path="/")
async def find_all(
    authorization: Annotated[None | str, Header()] = None,
):
    return JSONResponse(content={"message": "ok"}, status_code=status.HTTP_200_OK)
