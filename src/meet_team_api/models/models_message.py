from pydantic import BaseModel, Field


class MessageCreateRequest(BaseModel):
    """This model is to represent the request of message creation"""
    task_id: int
    creator_id: int
    description: str | None = Field(default=None)
