"""This is the module stores all user-related models"""

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """This is the model for register function"""
    name: str
    account: str
    password: str


class LoginRequest(BaseModel):
    """This is the model for login function"""
    account: str
    password: str
