import string

from langchain.agents import create_agent

from model import build_client_model
from prompts import build_system_prompt
from tools import ALL_TOOLS


def build_agent():
    model, provider = build_client_model()

    agent_kwargs: dict = {
        "model": model,
        "tools": ALL_TOOLS,
        "system_prompt": build_system_prompt(),
        "name": "Tickectmaster Agent"
    }

    return create_agent(**agent_kwargs)