"""This is the router for /user"""

import os
from typing import Annotated

import jwt
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse

from ...models.user import LoginRequest, RegisterRequest, UserInfoUpdate
from ..handlers import user as user_handler

user_router = APIRouter()


@user_router.get("/courses")
async def fetch_course(authorization: Annotated[str | None, Header()] = None):
    """
    Fetches the courses associated with a user.

    Parameters:
        authorization (str | None, Header()): The authorization header containing the bearer token.

    Returns:
        JSONResponse: A JSON response containing the fetched courses.

    Raises:
        HTTPException: If the bearer token is invalid or not provided.
        HTTPException: If there is an internal server error while fetching the courses.
    """
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
    """
    Fetches tasks for a user.

    Args:
        authorization (str | None, optional): The bearer token for authentication. Defaults to None.

    Raises:
        HTTPException: If the bearer token is invalid or not provided.
        HTTPException: If there is an internal server error while fetching the tasks.

    Returns:
        JSONResponse: A JSON response containing the fetched tasks.

    Status Codes:
        - 201 Created: If the tasks are successfully fetched.
        - 403 Forbidden: If the bearer token is invalid.
        - 500 Internal Server Error: If there is an internal server error.
    """
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
    """
    Retrieves information about a user with the given user ID.

    Parameters:
        user_id (int): The ID of the user to retrieve information for.
        authorization (Annotated[str | None, Header()], optional): The authorization token for the request. Defaults to None.

    Returns:
        JSONResponse: A JSON response containing the user information. The response has a status code of 200 if the request is successful.

    Raises:
        HTTPException: If the authorization token is invalid or missing. The exception has a status code of 403.

    """

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
async def find_self(authorization: Annotated[str | None, Header()] = None):
    """
    Retrieves information about the authenticated user.

    Parameters:
        authorization (Annotated[str | None, Header()], optional): The authorization token for the request. Defaults to None.

    Returns:
        JSONResponse: A JSON response containing the user information. The response has a status code of 200 if the request is successful.

    Raises:
        HTTPException: If the authorization token is invalid or missing. The exception has a status code of 403.

    """

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
    """
    Endpoint for user login.

    This route handles the login process for users. It expects a JSON payload containing the user's login information.
    The payload should be of the `LoginRequest` model.

    Parameters:
        - login_info (LoginRequest): The login information of the user.

    Returns:
        - JSONResponse: A JSON response containing the encoded JWT token and the user's ID.

    Raises:
        - HTTPException: If there is an error during the login process. The exception has a status code of 500.
        - HTTPException: If the login information is invalid. The exception has a status code of 400.

    """
    try:
        user_id = (await user_handler.login(**login_info.dict()))["id"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
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
    """
    Register a new user.

    This route handles the POST request to '/register' and registers a new user.
    It expects a JSON payload containing the user information.

    Parameters:
        user (RegisterRequest): The user information to be registered.

    Returns:
        JSONResponse: A JSON response with the registered user's ID if the registration is successful.
            The response has a status code of 201 (HTTP_201_CREATED).

    Raises:
        HTTPException: If there is an error during the registration process.
            The status code of the exception is 500 (HTTP_500_INTERNAL_SERVER_ERROR)
            and the detail of the exception contains the error message.
    """
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


@user_router.patch("/")
async def update_info(
    req: UserInfoUpdate, authorization: Annotated[str | None, Header()] = None
):
    """
    Updates the information of a user.

    Parameters:
        - req (UserInfoUpdate): The request object containing the updated user information.
        - authorization (Annotated[str | None, Header()], optional): The authorization header. Defaults to None.

    Returns:
        JSONResponse: A JSON response indicating the success or failure of the update.
            The response has a status code of 200 (HTTP_200_OK) and a message indicating the result of the update.

    Raises:
        HTTPException: If the authorization header is invalid or missing.
            The status code of the exception is 403 (HTTP_403_FORBIDDEN) and the detail of the exception is "Invalid Bearer Token".
    """
    print(authorization)
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

    succeed = await user_handler.update_info(user_id, req.description)

    return JSONResponse(
        {"data": {"message": "Ok" if succeed else "Failed"}},
        status_code=status.HTTP_200_OK,
    )
