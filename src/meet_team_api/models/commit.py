from pydantic import BaseModel, Field


class CommitCreateRequest(BaseModel):
    """This model is to represent the request of commit creation"""

    task_id: int
    reference_link: str | None = Field(default=None)
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)


class CommitCreateResponse(BaseModel):
    """This model is to represent the response of commit creation"""

    id: int
