"""This is the router for /group"""

import os
from typing import Annotated, Optional

import jwt
from fastapi import APIRouter, Header, Query, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from ...models.group import GroupCreateRequest, GroupUpdateRequest
from ..handlers import group as group_handler
from ..utils.get_userid import get_user_id
from ..utils.user_in_group import user_in_group
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
        ) from e
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
    try:
        return review_handler.get_group_members_and_reviews(group_id, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@group_router.get("/{group_id}/members")
async def find_members_by_name_pattern(
    group_id: int,
    name: Optional[str] = Query(default=None),
    authorization: Annotated[str, Header(name="authorization")] = None
):
    """
    Find the members whose name match the given pattern.

    Parameters:
        - group_id (int): The ID of the group.
        - name_pattern (str): The pattern to match the name.
        - token (str): The JWT token for authentication.

    Returns:
        - dict: The response containing the members' information.

    Raises:
        - HTTPException: If the group does not exist or the token is invalid or cannot be decoded.
    """
    try:
        user_in_group(user_id=get_user_id(authorization), group_id=group_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e
    try:
        members = await group_handler.find_members_by_name_pattern(
            group_id, name
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return JSONResponse(
        content={"data": {"members": members}}, status_code=status.HTTP_200_OK
    )
