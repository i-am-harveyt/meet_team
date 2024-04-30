from pydantic import BaseModel


class TaskCreateModel(BaseModel):
    name: str
    description: str | None
    assignee: int | None
    reviewer: int | None
