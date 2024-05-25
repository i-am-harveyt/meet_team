"""This is the module stores all user-related models"""

from pydantic import BaseModel, Field

from .course import ListedCourse

# Typedef
UserId = int


class UserRequestBaseModel(BaseModel):
    """This is the model for user-related request"""

    account: str
    password: str


class UserBaseModel(BaseModel):
    """This is the model for User model"""

    id: UserId
    name: str


class RegisterRequest(UserRequestBaseModel):
    """This is the model for register function"""

    name: str


class LoginRequest(UserRequestBaseModel):
    """This is the model for login function"""


class ListedUserItem(UserBaseModel):
    """some docstring"""


class UserInfoGuest(BaseModel):
    """This model is for getting user info in user page"""

    description: str
    avg_rating: float


class UserInfoSelf(BaseModel):
    """This model is for getting user info in user page"""

    account: str
    description: str
    courses: list[ListedCourse]
    avg_rating: float


class UserInfoUpdate(BaseModel):
    description: str | None = Field(default=None)
