import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODELOS = {
    "groq": "llama-3.3-70b-versatile"
}

LIMITE_APROVACAO = 80
LIMITE_TEMPO_MS = 3000

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY nao encontrada no .env")