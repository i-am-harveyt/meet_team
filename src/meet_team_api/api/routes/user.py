"""This is the router for /user"""

import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ...models.user import LoginRequest, RegisterRequest
from ..handlers.user import login, register

user_router = APIRouter()


@user_router.get("")
async def find_one():
    """Test routing"""
    return JSONResponse({"message": "Hello user"}, status_code=200)


@user_router.post("/register")
async def register_route(user: RegisterRequest):
    """register routing"""
    try:
        user_id = await register(**user.dict())
        return JSONResponse({"data": {"id": user_id}}, status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": {"message": str(e)}}, status_code=500)


@user_router.post("/login")
async def login_route(login_info: LoginRequest):
    """register routing"""
    print(login_info)
    try:
        user_id, user_name = await login(**login_info.dict())

        # If there's any authorization part, can be implemented here

        return JSONResponse(
            {"data": {"id": user_id, "name": user_name}}, status_code=200
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": {"message": str(e)}}, status_code=500)
