"""This is the initialization of routes module"""

from fastapi import APIRouter

from .user import user_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["User"])
