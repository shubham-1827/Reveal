from backend.services.parser_service import DecompiledFunction

current_functions: list[DecompiledFunction] = []


def store_functions(functions: list[DecompiledFunction]) -> None:
    global current_functions

    current_functions = functions


def get_functions() -> list[DecompiledFunction]:
    return current_functions


def get_function_by_name(name: str) -> DecompiledFunction | None:
    for function in current_functions:
        if function.name == name:
            return function

    return None
