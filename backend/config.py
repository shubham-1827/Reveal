import os

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

OPENROUTER_MODEL = "openai/gpt-oss-20b:free"

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "mistral:7b-instruct"

TIMEOUT = 250
