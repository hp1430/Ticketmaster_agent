import os
from dotenv import load_dotenv

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

TICKETMASTER_BASE_URL = os.getenv("TICKETMASTER_BASE_URL")