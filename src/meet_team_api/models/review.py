"""This is the module stores all review-related models"""

from datetime import datetime

from pydantic import BaseModel




class ReviewBaseModel(BaseModel):
    """This is the review base model"""
    id: int
    content: str
    create_at: datetime


class ReviewCreateRequest(BaseModel):
    """This model is to represent the request of review creation"""
    user_id: int
    group_id: int
    content: str


class ReviewCreateResponse(BaseModel):
    """This model is to represent the response of review creation"""
    id: int


class ReviewUpdateRequest(BaseModel):
    """This model is to represent the request of review update"""
    content: str


class ReviewUpdateResponse(BaseModel):
    """This model is to represent the response of review update"""
    pass


class ReviewGetResponse(ReviewBaseModel):
    """This model is to represent the response of getting a review"""
    pass


class ReviewListResponse(BaseModel):
    """This model is to represent the response of listing reviews"""
    reviews: list[ReviewBaseModel]
