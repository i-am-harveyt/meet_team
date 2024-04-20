"""This is the initialization of routes module"""

from fastapi import APIRouter

from .commit import commit_router
from .course import course_router
from .user import user_router
from .group import group_router
from .message import message_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(course_router, prefix="/course", tags=["Course"])
router.include_router(commit_router, prefix="/commit", tags=["Commit"])
router.include_router(group_router, prefix="/group", tags=["Group"])
router.include_router(message_router, prefix="/message", tags=["Message"])