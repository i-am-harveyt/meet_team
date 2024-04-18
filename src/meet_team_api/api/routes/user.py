"""This is the router for /user"""

import os
from typing import Annotated

import jwt
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse

from ...models.user import LoginRequest, RegisterRequest
from ..handlers.user import find_info, login, register

user_router = APIRouter()


@user_router.get("/{user_id}")
async def find_one(user_id: int, authorization: Annotated[str | None, Header()] = None):
    """find user info"""

    is_self = False
    if authorization is not None:
        payload = jwt.decode(
            authorization[7:], os.getenv("MEET_TEAM_JWT"), algorithms="HS256"
        )
        is_self = payload["id"][0] == user_id

    data = await find_info(user_id, is_self)

    return JSONResponse({"data": data}, status_code=status.HTTP_200_OK)


@user_router.post("/register")
async def register_route(user: RegisterRequest):
    """register routing"""
    try:
        user_id = await register(**user.dict())
        return JSONResponse(
            {"data": {"id": user_id}}, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@user_router.post("/login")
async def login_route(login_info: LoginRequest):
    """register routing"""
    try:
        user_id = await login(**login_info.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
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
        {"data": {"token": encoded_jwt}}, status_code=status.HTTP_200_OK
    )
