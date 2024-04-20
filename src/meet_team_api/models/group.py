"""This is the module stores all model-related models"""

from pydantic import BaseModel

from .course import CourseId
from .user import UserId

GroupId = int


class GroupBaseModel(BaseModel):
    """This is the base model"""

    id: GroupId
    course_id: CourseId


class GroupInfo(GroupBaseModel):
    """This is the contains group info"""

    group_name: str
    members_id: list[UserId]


class GroupJoinRequest(GroupBaseModel):
    """docstring"""
