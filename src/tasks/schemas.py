from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBaseSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=150, description="Title of the task")
    description: Optional[str] = Field(None, max_length=500, description="Description of the task")
    is_completed: bool = Field(..., description="Whether the task is completed")


class TaskCreateSchema(TaskBaseSchema):
    pass

class TaskUpdateSchema(TaskBaseSchema):
    pass

class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="ID of the task")
    created_at: datetime = Field(..., description="Created at of the task")
    updated_at: datetime = Field(..., description="Updated at of the task")

