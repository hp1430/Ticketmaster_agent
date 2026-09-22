from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader, select_autoescape

from configs.server_config import AGENT_NAME, PROMPTS_DIR
from tools import tool_catalog

_env = Environment(
    loader = FileSystemLoader(PROMPTS_DIR),
    autoescape=select_autoescape(enabled_extensions=()),
    trim_blocks=True,
    lstrip_blocks=True
)

def render_template(template_name: str, **context) -> str:
    return _env.get_template(template_name).render(**context)

def build_system_prompt(
    *,
    agent_name: str = AGENT_NAME,
    extra_guidance: str = ""
) -> str:
    now = datetime.now(timezone.utc)
    return render_template(
        "system_prompt.jinja",
        agent_name=agent_name,
        extra_guidance=extra_guidance,
        tools=tool_catalog(),
        current_datetime_utc=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        current_date=now.strftime("%Y-%m-%d"),
        current_day=now.strftime("%A"),
        current_year=now.year,
    )