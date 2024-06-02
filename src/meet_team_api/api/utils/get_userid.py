"""
This module contains the function `get_user_id` that extracts the user ID from a JWT token.
"""

import os
import jwt

from fastapi import status, HTTPException


def get_user_id(token: str) -> int:
    """
    Extracts the user ID from a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        int: The user ID extracted from the token.

    Raises:
        HTTPException: If the token is invalid or cannot be decoded.
    """
    try:
        secret_key = os.getenv("MEET_TEAM_JWT")
        payload = jwt.decode(token[7:], secret_key, algorithms=["HS256"])
        return int(payload["id"])
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from e
