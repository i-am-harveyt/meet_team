"""This is the route for commit"""

import os
from typing import Annotated

import jwt
from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from ...models.commit import CommitCreateRequest, CommitCreateResponse
from ..handlers import commit

commit_router = APIRouter()


@commit_router.post("/")
async def create(
    req: CommitCreateRequest, authorization: Annotated[str | None, Header()]
) -> CommitCreateResponse:
    """This route if to find all commits given the group"""
    try:
        assert isinstance(authorization, str)
        payload = jwt.decode(
            authorization[7:], os.getenv("MEET_TEAM_JWT"), algorithms=["HS256"]
        )
        user_id = payload["id"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Bearer Token",
        ) from e

    try:
        new_commit_id = await commit.create(
            user_id, req.task_id, req.title, req.description, req.reference_link
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e

    return JSONResponse(
        content={"commit": {"id": new_commit_id}}, status_code=status.HTTP_201_CREATED
    )
