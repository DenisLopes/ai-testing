import time
from groq import Groq
from utils.config import GROQ_API_KEY, MODELOS


class ClienteIA:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def perguntar(self, pergunta: str) -> dict:
        inicio = time.time()

        resposta = self.client.chat.completions.create(
            model=MODELOS["groq"],
            max_tokens=500,
            messages=[{"role": "user", "content": pergunta}]
        )

        return {
            "texto": resposta.choices[0].message.content,
            "tempo_ms": round((time.time() - inicio) * 1000, 2),
            "modelo": MODELOS["groq"]
        }