from backend.services.ai_provider import (
    generate,
)


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
    return generate(build_polish_prompt(code))
