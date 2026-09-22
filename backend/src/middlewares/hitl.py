from langchain.agents.middleware import HumanInTheLoopMiddleware 

def build_hitl_middleware() -> HumanInTheLoopMiddleware:
    return HumanInTheLoopMiddleware(
        interrupt_on={
            "search_events": {
                "allowed_decisions": [
                    "approve",
                    "reject"
                ]
            },
            "get_event_details": {
                "allowed_decisions": [
                    "approve",
                    "reject"
                ]
            },
            "search_venues_tool": {
                "allowed_decisions": [
                    "approve",
                    "reject"
                ]
            },
            "get_venue_details_tool": {
                "allowed_decisions": [
                    "approve",
                    "reject"
                ]
            },
        },
        description_prefix="Agent needs your approval to move ahead."
    )