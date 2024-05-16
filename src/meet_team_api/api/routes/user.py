"""This is the router for /user"""

import os
from typing import Annotated

import jwt
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse

from ...models.user import LoginRequest, RegisterRequest
from ..handlers import user as user_handler

user_router = APIRouter()


@user_router.get("/courses")
async def fetch_course(authorization: Annotated[str | None, Header()] = None):
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
        courses = await user_handler.fetch_course(user_id)
        return JSONResponse(
            {"data": {"course": courses}}, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@user_router.get("/tasks")
async def fetch_tasks(authorization: Annotated[str | None, Header()] = None):
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
        tasks = await user_handler.fetch_tasks(user_id)
        return JSONResponse(
            {"data": {"tasks": tasks}}, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@user_router.get("/{user_id}")
async def find_one(user_id: int, authorization: Annotated[str | None, Header()] = None):
    """find user info"""

    is_self = False
    try:
        assert isinstance(authorization, str)
        payload = jwt.decode(
            authorization[7:], os.getenv("MEET_TEAM_JWT"), algorithms="HS256"
        )
        is_self = payload["id"] == user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Bearer Token",
        ) from e

    data = await user_handler.find_info(user_id, is_self)

    return JSONResponse({"data": data}, status_code=status.HTTP_200_OK)


@user_router.get("/")
async def find_one(authorization: Annotated[str | None, Header()] = None):
    """find user info"""

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

    data = await user_handler.find_info(user_id, True)

    return JSONResponse({"data": data}, status_code=status.HTTP_200_OK)


@user_router.post("/login")
async def login(login_info: LoginRequest):
    """register routing"""
    try:
        user_id = (await user_handler.login(**login_info.dict()))["id"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login Failed"
        ) from e
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Account or Password",
        )

    # If there's any authorization part, can be implemented here
    encoded_jwt = jwt.encode(
        {"id": user_id}, os.getenv("MEET_TEAM_JWT"), algorithm="HS256"
    )

    return JSONResponse(
        {"data": {"token": encoded_jwt, "user": {"id": user_id}}},
        status_code=status.HTTP_200_OK,
    )


@user_router.post("/register")
async def register(user: RegisterRequest):
    """register routing"""
    try:
        user_id = await user_handler.register(**user.dict())
        return JSONResponse(
            {"data": {"id": user_id}}, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@user_router.patch("/user")
async def update_info():
    pass
