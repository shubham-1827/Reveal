from backend.services.parser_service import (
    DecompiledFunction,
)

from backend.services.ai_provider import (
    generate,
)

SELECTION_RATIO = 0.20

MIN_FUNCTIONS = 8

MAX_FUNCTIONS = 18

MAX_CODE_CHARS = 10000


def calculate_selection_count(
    total_functions: int,
) -> int:

    count = int(total_functions * SELECTION_RATIO)

    count = max(
        count,
        MIN_FUNCTIONS,
    )

    count = min(
        count,
        MAX_FUNCTIONS,
    )

    return count


def calculate_function_score(
    function: DecompiledFunction,
) -> int:

    score = 0

    code = function.code.lower()

    # main is important
    if function.name == "main":
        score += 100

    # larger functions matter more
    score += min(
        len(code) // 200,
        20,
    )

    # loops indicate processing
    score += code.count("for")
    score += code.count("while")

    # conditions indicate logic
    score += code.count("if")

    # string handling
    if "string" in code:
        score += 5

    if "char" in code:
        score += 5

    # file handling
    if "file" in code:
        score += 8

    if "fopen" in code:
        score += 10

    # input/output behavior
    if "printf" in code:
        score += 4

    if "scanf" in code:
        score += 4

    return score


def select_summary_functions(
    functions: list[DecompiledFunction],
) -> list[DecompiledFunction]:

    if not functions:
        return []

    selection_count = calculate_selection_count(len(functions))

    selected = []

    # Always include main
    for function in functions:

        if function.name == "main":
            selected.append(function)

    # Highest scored functions
    ranked = sorted(
        functions,
        key=calculate_function_score,
        reverse=True,
    )

    for function in ranked:

        if function not in selected:
            selected.append(function)

    # Add medium-sized functions
    medium = sorted(
        functions,
        key=lambda f: abs(len(f.code) - 800),
    )

    for function in medium:

        if function not in selected:
            selected.append(function)

    # Remove duplicates
    unique = []

    for function in selected:

        if function not in unique:
            unique.append(function)

    return unique[:selection_count]


def build_summary_context(
    functions: list[DecompiledFunction],
) -> str:

    output = ""

    for function in functions:

        output += f"Function: " f"{function.name}\n\n"

        output += function.code

        output += "\n\n"

    return output[:MAX_CODE_CHARS]


def build_summary_prompt(
    code_context: str,
) -> str:

    return f"""
Analyze the following reverse engineered
C code and generate a beginner-friendly
markdown executable summary.

Rules:
- Explain only visible behavior
- Avoid speculation
- Do not include code snippets
- Do not mention memory addresses
- Use markdown headings
- Use markdown bullet points
- Keep summary high-level
- Mention uncertainty when needed
- Never assume malware behavior
- Never treat strings as executable identity

Write between 400 and 500 words.

Structure:

# Executable Overview

# Main Behavior

# Important Logic Patterns

# User Interaction

# Overall Assessment

Code:

{code_context}
"""


def generate_summary(
    functions: list[DecompiledFunction],
) -> str:

    selected_functions = select_summary_functions(functions)

    code_context = build_summary_context(selected_functions)

    prompt = build_summary_prompt(code_context)

    return generate(prompt)
