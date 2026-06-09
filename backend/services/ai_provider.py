import requests

from backend.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_URL,
    OPENROUTER_MODEL,
    OLLAMA_URL,
    OLLAMA_MODEL,
    TIMEOUT,
)


def generate(
    prompt: str,
) -> str:

    try:

        return generate_openrouter(
            prompt,
        )

    except Exception as error:

        print(f"[AI Provider] " f"OpenRouter failed: {error}")

        return generate_ollama(
            prompt,
        )


def generate_openrouter(
    prompt: str,
) -> str:

    if not OPENROUTER_API_KEY:

        raise RuntimeError("OpenRouter API key not configured")

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": (f"Bearer {OPENROUTER_API_KEY}"),
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        },
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"OpenRouter error: " f"{response.status_code}\n" f"{response.text}"
        )

    data = response.json()

    try:

        return data["choices"][0]["message"]["content"].strip()

    except (
        KeyError,
        IndexError,
        TypeError,
    ):

        raise RuntimeError("Invalid OpenRouter response")


def generate_ollama(
    prompt: str,
) -> str:

    payload = {
        "model": OLLAMA_MODEL,
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

        raise RuntimeError("Ollama request timed out")

    except requests.exceptions.ConnectionError:

        raise RuntimeError("Ollama is not running")

    if response.status_code != 200:

        raise RuntimeError("Failed to get Ollama response")

    data = response.json()

    response_text = data.get(
        "response",
    )

    if not response_text:

        raise RuntimeError("Invalid Ollama response")

    return response_text.strip()


# testing openrouter working or not
if __name__ == "__main__":
    response = generate_openrouter("one liner greetings")
    print(response)
