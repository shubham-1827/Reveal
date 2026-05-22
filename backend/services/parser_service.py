import re

from backend.models.function_model import (
    DecompiledFunction,
)

FUNCTION_HEADER_PATTERN = re.compile(
    r"/\*\s*Function:\s*(.*?)\s*@\s*0x(.*?)\s*\*/",
    re.MULTILINE,
)


def parse_decompiled_file(
    file_path: str,
) -> list[DecompiledFunction]:

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    matches = list(FUNCTION_HEADER_PATTERN.finditer(content))

    functions = []

    for index, match in enumerate(matches):

        function_name = match.group(1).strip()

        address = match.group(2).strip()

        code_start = match.end()

        if index + 1 < len(matches):
            code_end = matches[index + 1].start()
        else:
            code_end = len(content)

        function_code = content[code_start:code_end].strip()

        functions.append(
            DecompiledFunction(
                name=function_name,
                address=address,
                code=function_code,
            )
        )

    return functions
