"""This is the module stores all course-related models"""

from pydantic import BaseModel, Field

CourseId = int


class CourseBaseModel(BaseModel):
    """Some docstring"""

    id: CourseId
    name: str


class ListedCourse(CourseBaseModel):
    """Some docstring"""

    name: str
    project_name: str
    contribution: str
    rating: float


class CreateCourseRequest(BaseModel):
    """Some docstring"""

    name: str
    year: int
    semester: int


class UpdateCourseRequest(BaseModel):
    """The request used for the update of the course"""

    id: CourseId
    name: str | None
    description: str | None = Field(default=None)
