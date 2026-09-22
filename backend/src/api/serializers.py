from api.schema import ChatResponse
from schemas.agent_result import AgentTurnResult


def serialize_result(
        result: AgentTurnResult,
        thread_id: str
) -> ChatResponse:
    """Converting the llm response to a format to return to client"""
    structured = None

    if result.structured is not None:
        structured = {
            "status": result.structured.status,
            "summary": result.structured.summary
        }

    if result.pending_interrupt is not None:
        return ChatResponse(
            status="approval_required",
            thread_id=thread_id,
            text=result.text or "",
            structured=structured,
            pending_interrupt=result.pending_interrupt
        )

    return ChatResponse(
        status="completed",
        thread_id=thread_id,
        text=result.text or "",
        structured=structured,
        pending_interrupt=None
    )