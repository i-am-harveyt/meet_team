"""This is the router for /group"""

import os
from typing import Annotated

import jwt
from fastapi import APIRouter, Header, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from ...models.group import GroupCreateRequest, GroupUpdateRequest
from ..handlers import group as group_handler
from ..utils.get_userid import get_user_id
from ..handlers import review as review_handler

group_router = APIRouter()


@group_router.post("/")
async def create(
    req: GroupCreateRequest, authorization: Annotated[str | None, Header()]
):
    """This function is to handle the routing of creating group given information"""
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
        new_group_id = await group_handler.create(
            req.course_id, user_id, req.name, req.description
        )
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return JSONResponse(
        content={
            "group": {
                "id": new_group_id,
                "course_id": req.course_id,
            }
        },
        status_code=status.HTTP_201_CREATED,
    )


@group_router.get("/")
async def info(group: int, authorization: Annotated[str | None, Header()]):
    """This funtion is to get group info"""
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
        data = await group_handler.find_one(group, user_id)
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e
    return JSONResponse(content={"data": data}, status_code=status.HTTP_200_OK)


@group_router.patch("/")
async def update(
    req: GroupUpdateRequest, authorization: Annotated[str | None, Header()]
):
    """This route provide update function toward course"""
    try:
        assert isinstance(authorization, str)
        payload = jwt.decode(
            authorization[7:], os.getenv("MEET_TEAM_JWT"), algorithms="HS256"
        )
        user_id = payload["id"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Bearer Token",
        ) from e

    try:
        group_id = await group_handler.update(
            user_id, req.id, req.name, req.description
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return JSONResponse(
        content={"data": {"group": {"id": group_id}}}, status_code=status.HTTP_200_OK
    )


@group_router.post("/{group_id}/join")
async def join(group_id: int, authorization: Annotated[str | None, Header()]):
    try:
        assert isinstance(authorization, str)
        payload = jwt.decode(
            authorization[7:], os.getenv("MEET_TEAM_JWT"), algorithms="HS256"
        )
        user_id = payload["id"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Bearer Token",
        ) from e

    try:
        succeed = await group_handler.join(user_id, group_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return JSONResponse(
        content={"data": {"message": "Ok" if succeed else "Failed"}},
        status_code=status.HTTP_200_OK if succeed else status.HTTP_403_FORBIDDEN,
    )


@group_router.get("/{group_id}/review")
async def get_group_members_and_reviews(
    group_id: int, authorization: Annotated[str, Header(name="Authorization")]
):
    """
    Get the group members and their reviews.

    Parameters:
        - group_id (int): The ID of the group.
        - token (str): The JWT token for authentication.

    Returns:
        - dict: The response containing the group members and their reviews.

    Raises:
        - HTTPException: If the group does not exist or the token is invalid or cannot be decoded.
    """
    user_id = get_user_id(authorization)
    return review_handler.get_group_members_and_reviews(group_id, user_id)
