from typing import Any
import asyncio
import uuid

from agent import build_agent
from memory import thread_config
from model import select_provider
from runtime import format_interrupt, resume_turn, start_turn
from schemas.agent_result import AgentTurnResult

def _ask_yes_or_no(name: str) -> bool:
    while True:
        answer = input(f"Allow {name}? (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer with 'y' or 'n'.", flush=True)

def _prompt_decision(pending: dict[str, Any]) -> list[dict]:
    print("\n--- Human-in-the-loop ---", flush=True)
    print(format_interrupt(pending), flush=True)
    requests = pending.get("action_requests") or []
    decisions: list[dict] = []
    for action in requests:
        name = action.get("name", "tool")
        approved = _ask_yes_or_no(name)
        if approved:
            decisions.append({
                "type": "approve"
            })
        else:
            decisions.append({
                "type": "reject",
                "message": (
                    f"User declined {name}. Do not immediately retry the same tool call"
                    "Explain what failed or ask the user"
                )
            })
    print("-----------------------------------\n", flush=True)
    return decisions

async def _drain(agent, result: AgentTurnResult, config: dict) -> AgentTurnResult:
    while result.pending_interrupt is not None:
        decision = _prompt_decision(result.pending_interrupt)
        result = await resume_turn(agent, decision, config)
    return result

async def chat() -> None:
    agent = build_agent()
    provider = select_provider()
    config = thread_config(str(uuid.uuid4()))

    print(f"Provider: {provider.name} . {provider.model}")
    print("Type 'exit', 'quit', 'q' to stop.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            break

        if not user_input:
            continue

        try:
            initial_result = await start_turn(agent, user_input, config)
            result = await _drain(agent, initial_result, config)
        except RuntimeError as e:
            print(f"LLM: {e}\n")
            continue
        except Exception as e:
            print(f"LLM: {type(e).__name__}: {e}\n")
            continue

        print(f"LLM: {result.text or '(no text)'}")

        if result.structured:
            print(
                f"  Summary={result.structured.status}\n"
                f"{result.structured.summary}"
            )
        print("\n-----------------------------------\n")

if __name__ == "__main__":
    asyncio.run(chat())
        