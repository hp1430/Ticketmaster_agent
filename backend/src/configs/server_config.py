import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

TICKETMASTER_BASE_URL = os.getenv("TICKETMASTER_BASE_URL")

PROJECT_ROOT = Path(__file__).parent.parent.parent

PROMPTS_DIR = PROJECT_ROOT / "prompts"

AGENT_NAME = os.getenv("AGENT_NAME", "Ticketmaster Buddy")

MAX_MODEL_CALLS_PER_RUN = int(os.getenv("MAX_MODEL_CALLS_PER_RUN", "10"))

def hitl_enabled() -> bool:
    return os.getenv("HITL_ENABLED", "true").lower() in {"1", "true", "yes"}