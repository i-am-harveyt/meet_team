"""This is the route for task"""

import os

import jwt
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Header
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from ...api.handlers import task
from ...models.task import TaskCreateModel

task_router = APIRouter()


@task_router.get("/all")
async def find_all(
    group: int,
    me: bool = False,
    authorization: Annotated[None | str, Header()] = None,
):
    """This function find all tasks given group_id and the if `self` or not"""
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
        data = await task.find_all(group, user_id, me)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're not in this group",
        ) from e
    return JSONResponse(content=data, status_code=200)


@task_router.get("/")
async def find_one(
    taskId: int,
    authorization: Annotated[None | str, Header()] = None,
):
    """This function find one task given task id"""
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
        data = await task.find_one(taskId, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e
    return JSONResponse(content=data, status_code=200)


@task_router.post("/{group_id}")
async def create(
    req: TaskCreateModel,
    group_id: int,
    authorization: Annotated[None | str, Header()] = None,
):
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
        new_id = await task.create(
            user_id, group_id, req.name, req.description, req.assignee, req.reviewer
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Bearer Token",
        ) from e
    return JSONResponse(content={"task": {"id": new_id}})
