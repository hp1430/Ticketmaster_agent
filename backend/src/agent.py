import string

from langchain.agents import create_agent

from configs.server_config import AGENT_NAME, hitl_enabled
from memory import make_checkpointer
from middlewares.build_middlewares import build_middlewares
from model import build_client_model
from prompts import build_system_prompt
from tools import tool_catalog


def build_agent(
    *,
    enable_hitl: bool | None = None,
    extra_guidance: str = "",
):
    model, provider = build_client_model()
    checkpointer = make_checkpointer()
    use_hitl = hitl_enabled() if enable_hitl is None else enable_hitl
    agent_name = AGENT_NAME

    agent_kwargs: dict = {
        "model": model,
        "tools": tool_catalog(),
        "system_prompt": build_system_prompt(extra_guidance=extra_guidance, agent_name=agent_name),
        "middleware": build_middlewares(enable_hitl=use_hitl),
        "checkpointer": checkpointer,
        "name": "Tickectmaster Agent"
    }

    return create_agent(**agent_kwargs)