from datetime import date
import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")


APP_NAME = "returnshield-api"
API_PREFIX = "/api"

# Fixed demo date keeps ORD-1045 stable for the hackathon flow.
DEMO_TODAY = date(2026, 5, 20)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
