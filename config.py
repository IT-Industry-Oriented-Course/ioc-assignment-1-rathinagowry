import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "openai/gpt-oss-20b:free"

OPENAI_BASE_URL = "https://openrouter.ai/api/v1"

DRY_RUN_DEFAULT = True
