import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "mistral:7b-instruct"

TIMEOUT = 120


def build_prompt(
    function_name: str,
    code: str,
) -> str:

    return f"""
You are explaining reverse engineered C code.

Requirements:
- Explain only visible logic.
- Do not hallucinate behavior.
- Do not invent malware functionality.
- Keep explanations beginner-friendly.
- Format the explanation using markdown.
- Use headings and bullet points where appropriate.
- Mention:
  - function purpose
  - parameters
  - return value
  - loops
  - conditions
  - important logic

Function:
{function_name}

Code:
{code}
"""


def explain_function(
    function_name: str,
    code: str,
) -> str:

    prompt = build_prompt(
        function_name,
        code,
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
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

    explanation = data.get("response")

    if not explanation:
        raise RuntimeError("Invalid AI response")

    return explanation.strip()
