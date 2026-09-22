from typing import Any
from langgraph.types import Command

from messages import last_ai_text, last_tool_text
from schemas.agent_result import AgentTurnResult, TurnSummary

def _as_summary(value: Any) -> TurnSummary | None:
    if value is None:
        return None
    if isinstance(value, TurnSummary):
        return value
    if isinstance(value, dict):
        try:
            return TurnSummary.model_validate(value)
        except Exception:
            return None
    return None

def parse_invoke_result(result: Any) -> AgentTurnResult:
    interrupts = tuple(getattr(result, "interrupts", ()) or ())
    value = getattr(result, "value", result)

    if not isinstance(value, dict):
        value = {}

    messages = value.get("messages") or []

    if interrupts:
        payload = interrupts[0].value
        return AgentTurnResult(
            text="",
            structured=None,
            messages=messages,
            pending_interrupt=payload
        )

    return AgentTurnResult(
        text=last_ai_text(messages) or last_tool_text(messages),
        structured =_as_summary(value.get("structured_response")),
        messages=messages,
        pending_interrupt=None
    )

async def start_turn(agent, user_text: str, config: dict) -> AgentTurnResult:
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        },
        config=config,
        version="v2"
    )
    return parse_invoke_result(result)

async def resume_turn(agent, decisions: list[dict], config: dict) -> AgentTurnResult:
    result = await agent.ainvoke(
        Command(resume={
            "decisions": decisions
        }),
        config=config,
        version="v2"
    )
    return parse_invoke_result(result)

def format_interrupt(pending: dict[str, Any]) -> str:
    requests = pending.get("action_requestes") or []
    lines = []

    for index, action in enumerate(requests, start=1):
        name = action.get("name", "?")
        args = dict(action.get("args") or {})
        description = action.get("description", "?")
        lines.append(f"{index}. {name} ({description})")
        for key, value in args.items():
            preview = str(value)
            if "\n" in preview:
                lines.append(f"    {key}:")
                for body_line in preview.splitlines():
                    lines.append(f"     {body_line}")
                continue

            if len(preview) > 240:
                   preview = preview[:240] + "..."
            lines.append(f"     {key}: {preview}")
    return "\n".join(lines) if lines else str(pending)