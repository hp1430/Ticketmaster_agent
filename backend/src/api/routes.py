import uuid

from fastapi import APIRouter, HTTPException

from agent import build_agent
from api.schema import ApprovalRequest, ChatRequest, ChatResponse
from api.serializers import serialize_result
from memory import thread_config
from runtime import resume_turn, start_turn


router = APIRouter(prefix="/api", tags=["agent"])

agent = build_agent()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    thread_id = request.thread_id or str(uuid.uuid4())

    config = thread_config(thread_id)

    try:
        result = await start_turn(
            agent,
            request.message,
            config
        )

        return serialize_result(result, thread_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {e}"
        ) from e

@router.post("/chat/approve", response_model=ChatResponse)
async def approve(
    request: ApprovalRequest
) -> ChatResponse:
    config = thread_config(request.thread_id)

    decisions = [
        decision.model_dump(exclude_none=True) for decision in request.decisions
    ]

    try:
        result = await resume_turn(
            agent,
            decisions,
            config
        )

        return serialize_result(
            result,
            request.thread_id,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc