import requests

# 🔑 IMPORTANTE: acá va tu API KEY
API_KEY = "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"

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def generar_prompt_resumen(texto: str) -> str:
    return f"""
Resumí el siguiente texto de forma clara y simple.No dejes frases incompletas.Maximo 20 lineas:

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

