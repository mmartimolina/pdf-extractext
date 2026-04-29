import requests
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener API KEY desde entorno
API_KEY = os.getenv("API_KEY")

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def generar_prompt_resumen(texto: str) -> str:
    return f"""
Resumí el siguiente texto de forma clara y simple. No dejes frases incompletas. Máximo 20 líneas:

{texto}
"""


def summarize_text(texto: str) -> str:
    prompt = generar_prompt_resumen(texto)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error generando resumen: {str(e)}"

