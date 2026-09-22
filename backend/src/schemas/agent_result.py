from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, Field


class TurnSummary(BaseModel):
    """What the coding agent didi in this turn?"""

    summary: str = Field(
        description="A concise summary of what the coding agent did in this turn"
    )

    status: Literal["ok", "needs_input", "failed"] = Field(
        description="ok if request is done, needs_input if you must ask the user, failed if the request failed"
    )

@dataclass
class AgentTurnResult:
    text: str   # agent's reply
    structured: TurnSummary | None
    messages: list[Any]
    pending_interrupt: dict[str, Any] | None