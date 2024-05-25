"""This is the module stores all model-related models"""

from pydantic import BaseModel, Field

from .course import CourseId

GroupId = int


class GroupCreateRequest(BaseModel):
    """This Model represent the attributes in the request"""

    course_id: CourseId
    name: str
    description: str | None = Field(default=None)


class GroupUpdateRequest(BaseModel):
    """The request used for the update of the group"""

    id: GroupId
    name: str
    description: str | None = Field(default=None)


class GroupJoinRequest(BaseModel):
    """The request used for user joining a group"""

    group_id: GroupId
