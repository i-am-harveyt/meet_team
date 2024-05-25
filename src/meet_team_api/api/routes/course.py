"""This is the router for /course"""

import os
from typing import Annotated, Optional

import jwt
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse

from ...models.course import CourseId, CreateCourseRequest, UpdateCourseRequest
from ..handlers import course, group

course_router = APIRouter()


@course_router.get("/{course_id}")
async def find_one(
    authorization: Annotated[str | None, Header()],
    course_id: int = -1,
    groups: bool = False,
):
    """This is for finding specific course's information"""
    ret = {"data": None}
    print(course_id)
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
        course_info = await course.find_course(course_id, user_id)
        ret["data"] = {"course": course_info}
    except Exception as e:
        raise HTTPException(
            detail={"message": "Wrong course id", "error": str(e)},
            status_code=status.HTTP_403_FORBIDDEN,
        ) from e

    if groups:
        try:
            groups_info = await group.find_by_course(course_id)
            ret["data"]["groups"] = groups_info
        except Exception as e:
            raise HTTPException(
                detail={"message": "Fetch Groups Failed", "error": str(e)},
                status_code=status.HTTP_403_FORBIDDEN,
            ) from e

    return JSONResponse(ret, status_code=status.HTTP_200_OK)


@course_router.get("/")
async def find_all(
    searchTerm: Optional[str] = None, offset: int = 0, limit: int = 10
):
    """This is the for listing the courses"""
    courses = []
    meta = {}
    try:
        courses = await course.find_all(offset, limit, searchTerm)
        meta = {
            "offset": offset,
            "limit": limit,
        }
    except Exception as e:
        raise HTTPException(
            detail={"message": str(e)},
            status_code=status.HTTP_403_FORBIDDEN,
        ) from e

    return JSONResponse(
        {
            "data": {"courses": courses, "meta": meta},
        },
        status.HTTP_200_OK,
    )


@course_router.post("/{course_id}/join")
async def join(course_id: CourseId, authorization: Annotated[str | None, Header()]):
    """This router is for adding a user into a course"""
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
        new_course_id = await course.join(course_id, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return JSONResponse(
        {"data": {"course": {"id": new_course_id}}}, status_code=status.HTTP_200_OK
    )


@course_router.post("/")
async def create(
    req: CreateCourseRequest, authorization: Annotated[str | None, Header()]
):
    """This route is to create a course"""

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
        new_course_id = await course.create_course(
            req.name, req.year, req.semester, user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return JSONResponse(
        {"data": {"course": {"id": new_course_id}}}, status_code=status.HTTP_201_CREATED
    )


@course_router.patch("/")
async def update_info(
    req: UpdateCourseRequest, authorization: Annotated[str | None, Header()]
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
        course_id = await course.update_course(
            user_id, req.id, req.name, req.description
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e

    return JSONResponse(
        content={"data": {"course": {"id": course_id}}}, status_code=status.HTTP_200_OK
    )
