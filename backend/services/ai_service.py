from backend.services.ai_provider import (
    generate,
)


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

    return generate(
        prompt,
    )
