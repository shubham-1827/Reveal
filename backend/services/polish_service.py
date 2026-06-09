import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "mistral:7b-instruct"

TIMEOUT = 250


def build_polish_prompt(
    code: str,
) -> str:

    return f"""
Improve the readability of this decompiled C code.

Requirements:
- Preserve logic exactly.
- Preserve behavior exactly.
- Improve variable names.
- Improve parameter names.
- Improve formatting.
- Improve indentation.
- Improve readability.

Do not:
- Change functionality.
- Remove code.
- Add code.
- Rewrite algorithms.

Return only the improved C code.

Code:
{code}
"""


def polish_code(
    code: str,
) -> str:

    payload = {
        "model": MODEL_NAME,
        "prompt": build_polish_prompt(code),
        "stream": False,
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT,
        )

    except requests.exceptions.Timeout:
        raise RuntimeError("AI request timed out")

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Ollama is not running")

    if response.status_code != 200:
        raise RuntimeError("Failed to get AI response")

    data = response.json()

    polished_code = data.get("response")

    if not polished_code:
        raise RuntimeError("Invalid AI response")

    return polished_code.strip()
