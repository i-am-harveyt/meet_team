"""
This module contains the API router for the review resource.
"""

from typing import Annotated, Optional

from fastapi import APIRouter, Body, Header, Query
from ...models.user import UserId

from ..handlers import review as review_handler
from ..utils.get_userid import get_user_id

review_router = APIRouter()


@review_router.post("/{group_id}")
async def upsert_review(
    group_id: int,
    reviews: Annotated[dict, Body(...)],
    authorization: Annotated[str, Header(name="Authorization")],
):
    """
    This endpoint is used to upsert the review
    """
    user_id = get_user_id(authorization)
    return await review_handler.upsert_review(group_id, user_id, reviews)


@review_router.get("/user/")
async def get_user_review(
    user_id: Optional[str | UserId] = Query(default=None),
    authorization: Annotated[str, Header(name="Authorization")] = None,
) -> dict:
    """
    Retrieves the review for a specific user.

    Args:
        user_id (UserId): The ID of the user.
        authorization (str): The authorization token provided in the request header.

    Returns:
        dict: The review information for the specified user.

    Raises:
        None

    Notes:
        - The `authorization` parameter is used to obtain the owner ID for permission checks.
        - The `get_user_id` function is called to extract the owner ID from the provided authorization token.
        - The `review_handler.get_user_review` function is called to retrieve the review information for the specified user.
    """
    if user_id is None:
        user_id = get_user_id(authorization)
    return await review_handler.get_user_review(user_id)
