from pydantic import BaseModel
from typing import Optional

class WorkflowRequest(BaseModel):
    user_id: str
    message: str

class TaskCreate(BaseModel):
    title: str
    due_date: Optional[str] = None
    priority: Optional[str] = "medium"
