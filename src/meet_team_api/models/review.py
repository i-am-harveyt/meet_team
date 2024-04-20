"""This is the module stores all review-related models"""

from datetime import datetime

from pydantic import BaseModel


class ReviewBaseModel(BaseModel):
    """This is the review base model"""

    id: int
    content: str
    create_at: datetime
