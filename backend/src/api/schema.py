from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    thread_id: str | None = None

class ApprovalDecision(BaseModel):
    type: Literal["approve", "reject"]
    message: str | None = None

class ApprovalRequest(BaseModel):
    thread_id: str
    decisions: list[ApprovalDecision]

class ChatResponse(BaseModel):
    status: Literal["completed", "approval_required"]
    thread_id: str
    text: str = ""
    structured: dict[str, Any] | None = None
    pending_interrupt: dict[str, Any] | None = None